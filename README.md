##  KG entity embedding Service

This repo has APIs the can be used to access embeddings for all the DBpedia entities. The embeddings are indexed on Elasticsearch server. 
<br><br>

###  List of APIs

#### 1. Get entity embeddings
This API takes a list of entities as input and returns the embeddings of the given entities in response. It returns embeddings of first 10 unique entities and ignores the rest. 
```
         URL: /get-entity-embedding
      METHOD: GET
Request Body: {
                  "entities": Array of entities
              }
```

#### 2. Get elastic search entity embedding index properties
This API returns the list of properties of every document in the Elasticsearch index of entity embeddings. 
```
         URL: /get-entity-index-info
      METHOD: GET
```

#### 3. Get relation embeddings
This API takes a list of relations as input and returns the embeddings of the given entities in response. It returns embeddings of first 10 unique entities and ignores the rest. 
```
         URL: /get-relation-embedding
      METHOD: GET
Request Body: {
                  "relations": Array of relations
              }
```

#### 4. Get elastic search relation embedding index properties
This API returns the list of properties of every document in the Elasticsearch index of relation embeddings. 
```
         URL: /get-relation-index-info
      METHOD: GET
```

These APIs can be accessed from http://nel.cs.upb.de:5000/ on UPB network for now.
