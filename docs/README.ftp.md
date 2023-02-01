# Embeddings.cc data

This directory contains datasets provided at [embeddings.cc](https://embeddings.cc/).
The related code is on [GitHub](https://github.com/dice-group/embeddings.cc).
The data is stored at the [Hobbit FTP server](https://hobbitdata.informatik.uni-leipzig.de/embeddings_cc/).

## Datasets

Every dataset has an ID. The **dataset ID** consists of lower case characters and underscores. It is used to identify the dataset in storage solutions (e.g. Elasticsearch) and to identify corresponding files.
A good ID should describe a dataset and list relevant characteristics, which are e.g. the data sources and approaches used to compute the embeddings.

- An example of embeddings which is based on a Wikidata file dump from 2023, limited to 10,000 URIs and computed with  the SHALLOM approach could be `wikidata2023_shallom_10k`.
- An example of aligned embeddings from Wikidata and DBpedia from 2023, which were originally computed with the ConEx approach could be `dbpedia_wikidata_2023_conex_procrustes`.

A dataset consists of pairs of an **URI** and related **embeddings**. Embeddings are represented as a vector of floating-point numbers.


## File formats

For every dataset, the following files are required:

### Embeddings file

Every line contains floating-point numbers divided by a comma.
The line numbers are related to the URI line numbers.

Example:

```
0,1,2,3,4,5,6,7,8,9
1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,0.0
```

### URIs file

Every line contains a URI starting with `http://` or `https://`.
The line numbers are related to the embeddings line numbers.

Example:

```
http://example.com/0
http://example.com/1
```

## Compression

There are two scripts to directly read and write files in text or [bzip2](https://en.wikipedia.org/wiki/Bzip2) format:

- To produce data files, a [Python file writer](https://github.com/dice-group/embeddings.cc/blob/master/api/serialization/file_writer.py) is available on GitHub.
- An example [Python file reader](https://github.com/dice-group/embeddings.cc/blob/master/api/serialization/file_reader.py) is also available on GitHub.

You can also compress the text files with other approaches, e.g. [Zstandard (zstd)](https://facebook.github.io/zstd/).