##  KG entity embedding Service

This repo has APIs the can be used to access embeddings for KGE entities. The embeddings are indexed on Elasticsearch server. 
<br><br>

###  List of APIs

#### 1. Get entity embeddings
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




#### 2. Get neighbour entities and their embedding for an embedding vector
This API returns the 10 nearest neighbour of an embedding based on cosine distance.
```
         URL: /get-entity-embedding-neighbour
       METHOD: GET
Request Body: {
                  "indexname": Name of the index,
                  "embedding": Emdebbing vector
                  
              }
Sample request body:
{
    "indexname":"shallom_dbpedia_index",
    "embedding" : [0.02233588,
        0.010766734,
        0.02364266,
        -0.027576402,... 0.010766734]
}
```

These APIs can be accessed from http://unikge.cs.upb.de:5001/ on UPB network for now.
