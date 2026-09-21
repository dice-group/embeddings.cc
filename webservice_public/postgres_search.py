"""Wikidata, DBpedia and WDC autocomplete backed by entity_search."""

import atexit
import os
import threading

from flask import current_app
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


_pool_lock = threading.Lock()
LIMIT = 5
SOURCES = {'wikidata': 1, 'dbpedia': 4, 'wdc': 3}


def init_app(app):
    defaults = {
        'WIKIDATA_PG_HOST': '131.234.29.20',
        'WIKIDATA_PG_PORT': '5432',
        'WIKIDATA_PG_DATABASE': 'postgres',
        'WIKIDATA_PG_USER': 'postgres',
        'WIKIDATA_PG_PASSWORD': '',
        'WIKIDATA_FTS_MIN_SCORE': '0.05',
        'WIKIDATA_TRIGRAM_MIN_SCORE': '0.3',
    }
    for key, default in defaults.items():
        app.config.setdefault(key, os.getenv(key, default))


def get_pool():
    # Create lazily inside the serving worker, not before uWSGI forks.
    app = current_app._get_current_object()
    with _pool_lock:
        pool = app.extensions.get('wikidata_pg_pool')
        if pool is None:
            config = app.config
            if not config['WIKIDATA_PG_PASSWORD']:
                raise ValueError('Wikidata PostgreSQL password is not configured')
            pool = ConnectionPool(
                conninfo='',
                kwargs={
                    'host': config['WIKIDATA_PG_HOST'],
                    'port': int(config['WIKIDATA_PG_PORT']),
                    'dbname': config['WIKIDATA_PG_DATABASE'],
                    'user': config['WIKIDATA_PG_USER'],
                    'password': config['WIKIDATA_PG_PASSWORD'],
                    'connect_timeout': 3,
                    'options': '-c statement_timeout=1500 -c default_transaction_read_only=on',
                    'row_factory': dict_row,
                },
                min_size=0, max_size=4, timeout=3, max_waiting=16,
                open=True,
            )
            app.extensions['wikidata_pg_pool'] = pool
            atexit.register(pool.close)
        return pool


def search(search_term, source='wikidata'):
    """Try both FTS modes; use label typos only if neither scores well.

    FTS scores use ts_rank_cd normalization 32. They are ranking heuristics,
    not probabilities. The configurable cutoff should be tuned on real queries.
    Word similarity matches the input against the best portion of a label.
    The trigram predicate targets an existing pg_trgm index on label.
    """
    source_id = SOURCES[source]
    minimum = float(current_app.config['WIKIDATA_FTS_MIN_SCORE'])
    trigram_minimum = float(current_app.config['WIKIDATA_TRIGRAM_MIN_SCORE'])
    if not 0 <= minimum <= 1 or not 0 <= trigram_minimum <= 1:
        raise ValueError('Search score thresholds must be between zero and one')

    with get_pool().connection() as connection:
        queries = connection.execute(
            """
            SELECT plainto_tsquery('english', %(term)s)::text AS full_query,
                   (SELECT string_agg(quote_literal(lexeme) || ':*', ' & ')
                    FROM unnest(tsvector_to_array(
                        to_tsvector('english', %(term)s)
                    )) AS words(lexeme)) AS prefix_query
            """, {'term': search_term},
        ).fetchone()
        candidates = {}
        best_scores = []
        for mode in ('full_query', 'prefix_query'):
            query = queries[mode]
            rows = []
            if query:
                rows = connection.execute(
                    """
                    SELECT entity_iri, label, types,
                           ts_rank_cd(search_vector, %(query)s::tsquery, 32) AS score
                    FROM entity_search
                    WHERE source = %(source_id)s AND search_vector @@ %(query)s::tsquery
                    ORDER BY score DESC, label, entity_iri
                    LIMIT 5
                    """, {'query': query, 'source_id': source_id},
                ).fetchall()
            best_scores.append(max((row['score'] for row in rows), default=0))
            for row in rows:
                previous = candidates.get(row['entity_iri'])
                if previous is None or row['score'] > previous['score']:
                    candidates[row['entity_iri']] = row

        rows = sorted(candidates.values(), key=lambda row: (
            -row['score'], row['label'] or '', row['entity_iri'],
        ))
        if all(score < minimum for score in best_scores) or not rows:
            # SET LOCAL via set_config keeps the threshold scoped to this
            # transaction, without leaking settings into the pooled connection.
            connection.execute(
                "SELECT set_config('pg_trgm.word_similarity_threshold', %s, true)",
                (str(trigram_minimum),),
            )
            fuzzy_rows = connection.execute(
                """
                SELECT entity_iri, label, types,
                       word_similarity(%(term)s, label) AS score
                FROM entity_search
                WHERE source = %(source_id)s AND label %%> %(term)s
                ORDER BY score DESC, label, entity_iri
                LIMIT 5
                """, {'term': search_term, 'source_id': source_id},
            ).fetchall()
            # The two score scales are not comparable. Prefer qualifying typo
            # results to weak FTS results, then fill any remaining slots.
            seen = set()
            merged = []
            for row in fuzzy_rows + rows:
                if row['entity_iri'] not in seen:
                    seen.add(row['entity_iri'])
                    merged.append(row)
            rows = merged

    return [
        {'entity': row['entity_iri'], 'label': row['label'],
         'types': row['types'], 'source': source}
        for row in rows[:LIMIT]
    ]
