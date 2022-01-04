##  KG entity embedding Service

This repo has APIs the can be used to access embeddings for KGE entities. The embeddings are indexed on Elasticsearch server. 
<br><br>

###  List of APIs


#### 1. List all indexes
This API returns list of all available indexes on the elastic search server. 
```
         URL: /get-index-list
      METHOD: GET
Request Body: NA

```

#### 2. Get entity embeddings
This API takes a list of entities and index name as input and returns the embeddings of the given entities in response. It returns embeddings of first 10 unique entities and ignores the rest. 
```
         URL: /get-entity-embedding
      METHOD: GET
Request Body: {
                  "entities": Array of entities,
                  "indexname": Name of the index
              }
Sample request body:
{
    "indexname":"shallom_dbpedia_index",
    "entities" : ["/resource/Boeing_747_hull_losses"]
}
```

#### 3. Get neighbour entities and their embedding for an embedding vector
This API returns the 10 nearest neighbour of an embedding based on cosine distance.
```
         URL: /get-entity-embedding-neighbour
       METHOD: GET
Request Body: {
                  "indexname": Name of the index,
                  "embedding": Emdebbing vector,
                  "distmetric: Distance measure for neighbour search (Default : Cosine)                  
              }
Supported distance measures:
         Cosine Similarity : "cosine"
         Euclidean Distance : "l2"
Sample request body:
{
    "indexname":"shallom_dbpedia_index",
    "embedding" : [0.02233588,
        0.010766734,
        0.02364266,
        -0.027576402,... 0.010766734],
    "distmetric":"cosine"
}
```

#### 4. Get neighbour entities and their embedding using entity name
This API returns the 10 nearest neighbour of an entity based on cosine distance.
```
         URL: /get-entity-embedding-neighbour
       METHOD: GET
Request Body: {
                  "indexname": Name of the index,
                  "entity": Entity resource name
                  
              }
Sample request body:
{
    "indexname":"shallom_dbpedia_index",
    "entity" : "/resource/Boeing_747_hull_losses"
}
```
#### 5. Get index information
This API takes an index name and returns the all available information about the index(settings and mapping) 
```
         URL: /get-index-info
      METHOD: GET
Request Body: {
                  "indexname": Name of the index
              }
Sample request body:
{
    "indexname" : "shallom_dbpedia_index"
}
```

These APIs can be accessed from http://unikge.cs.upb.de:5001/ on UPB network for now.
