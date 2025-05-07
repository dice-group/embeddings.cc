import os
import json
import sys

proj_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)
sys.path.insert(0, proj_root)

from webservice_public import create_app, es
from webservice_public.random_extract import extract_uris

def main():
    os.environ.setdefault('FLASK_APP', 'webservice_public:create_app')
    app = create_app()

    with app.app_context():
        client = es.get_es()
        try:
            uris = extract_uris(
                client,
                index='whale',
                target=1000,
                size=100
            )
        except Exception as e:
            app.logger.error(f"Failed to extract URIs: {e}")
            uris = []

        out = os.path.join(app.instance_path, 'uris.json')
        os.makedirs(app.instance_path, exist_ok=True)
        with open(out, 'w') as f:
            json.dump(uris, f, indent=2)
        print(f"Wrote {len(uris)} URIs to {out}")

if __name__ == '__main__':
    main()