##  KG entity embedding Service

This repo has APIs the can be used to access embeddings for KGE entities. The embeddings are indexed on Elasticsearch server. 
<br><br>

###  Installations and index creation

1. Install Elastic Search 7.16 or above.
   Installation information is available on https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html
```
   wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
   sudo apt-get install apt-transport-https
   echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list 
   sudo apt-get update && sudo apt-get install elasticsearch
   sudo -i service elasticsearch start
```
2. Start Elastic Search server
```
   sudo -i service elasticsearch start
```
3. Create indexes using tsv embedding files
```
   Use Create_entity_index_tsv.py to create indexes for entity embedding files
   
   Change the following parameter in the Create_entity_index_tsv.py file.
   "index_name" : Name of the index (User's choice)
   "data_path" : Path to the embedding .tsv file
   "dim" : Number of dimension in the embedding vector
   
   Run Create_entity_index_tsv.py using nohup Python3 -u Create_entity_index_tsv.py &
   
   Use Create_relation_index_tsv.py to create indexes for relation embedding files
   
   Change the following parameter in the Create_entity_index_tsv.py file.
   "index_name" : Name of the index (User's choice)
   "data_path" : Path to the embedding .tsv file
   "dim" : Number of dimension in the embedding vector
    
   Run Create_relation_index_tsv.py using nohup Python3 -u Create_entity_index_tsv.py &
```
4. Start the service

```
With Docker

Build the docker image:
Run command : docker build . -t embeddingservice
Deploy the docker stack:
Run command :  docker stack deploy --compose-file docker-compose.yml embedding-service

Wihtout Docker 

Change the ES uri host from "172.18.0.1" to "localhost"
Run command : nohup python3 -u run.py &
```

###  List of APIs


#### 1. List all indexes
This API returns list of all available indexes on the elastic search server. 
```
         URL: /get-index-list
      METHOD: GET
Request Body: NA

curl -X GET http://unikge.cs.upb.de:5001/get-index-list

```
#### 2. Get index information
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
curl -X GET http://unikge.cs.upb.de:5001/get-index-info -H "Content-Type: application/json" -d '{"indexname":"shallom_dbpedia_index"}'
```
#### 3. Get entity embeddings
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
curl -X GET http://unikge.cs.upb.de:5001/get-entity-embedding -H "Content-Type: application/json" -d '{"indexname":"shallom_dbpedia_index","entities" : ["/resource/Boeing_747_hull_losses"]}'
```

#### 4. Get relation embeddings
This API takes a list of relations and index name as input and returns the embeddings of the given realtions in response. It returns embeddings of first 10 unique relations and ignores the rest. 
```
         URL: /get-relation-embedding
      METHOD: GET
Request Body: {
                  "relations": Array of entities,
                  "indexname": Name of the index
              }
Sample request body:
{
    "indexname":"shallom_dbpedia_index",
    "relations" : ["/resource/Boeing_747_hull_losses"]
}
curl -X GET http://unikge.cs.upb.de:5001/get-relation-embedding -H "Content-Type: application/json" -d '{"indexname":"shallom_dbpedia_index","relations" : ["/resource/Boeing_747_hull_losses"]}'
```

#### 5. Get all entities
This API returns list of entities of an index. 
```
         URL: /get-all-entity
      METHOD: POST
Request Body: {
                  "indexname": Name of the index,
                  "size" : Number of entities to search (Optional,Default : All)
              }

curl -X GET http://unikge.cs.upb.de:5001/get-all-entity -H "Content-Type: application/json" -d '{"indexname":"shallom_dbpedia_index","size" : 10}'

```

#### 6. Get all relations
This API returns list of relations of an index. 
```
         URL: /get-all-relation
      METHOD: POST
Request Body: {
                  "indexname": Name of the index,
                  "size" : Number of relations to search (Optional,Default : All)
              }

curl -X GET http://unikge.cs.upb.de:5001/get-all-relation -H "Content-Type: application/json" -d '{"indexname":"shallom_dbpedia_index","size" : 10}'

```

#### 7. Get neighbour entities/relations for an embedding vector
This API returns the 10 nearest neighbour of an embedding based on cosine distance.
```
         URL: /get-embedding-neighbour
       METHOD: GET
Request Body: {
                  "indexname": Name of the index,
                  "embedding": Emdebbing vector,
                  "distmetric: Distance measure for neighbour search (Optional,Default : Cosine)                  
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
curl -X GET http://unikge.cs.upb.de:5001/get-embedding-neighbour -H "Content-Type: application/json" -d '{"indexname":"shallom_dbpedia_index","embedding" : [0.02233588,
        0.010766734,
        0.02364266,
        -0.027576402,... 0.010766734],
    "distmetric":"cosine"}'
```



#### 8. Get neighbour entities and their embedding using entity uri
This API returns the 10 nearest neighbour of an entity based on cosine distance.
```
         URL: /get-entity-neighbour
       METHOD: GET
Request Body: {
                  "indexname": Name of the index,
                  "entity": Entity URI,
                  "distmetric: Distance measure for neighbour search (Optional,Default : Cosine)
              }
Sample request body:
{
    "indexname":"shallom_dbpedia_index",
    "entity" : "/resource/Boeing_747_hull_losses",
    "distmetric":"cosine"    
}
curl -X GET http://unikge.cs.upb.de:5001/get-entity-neighbour -H "Content-Type: application/json" -d '{"indexname":"shallom_dbpedia_index","entity" : "/resource/Boeing_747_hull_losses","distmetric":"cosine"}'
```
#### 9. Get neighbour realtions and their embedding using relation uri
This API returns the 10 nearest neighbour of an entity based on cosine distance.
```
         URL: /get-relation-neighbour
       METHOD: GET
Request Body: {
                  "indexname": Name of the index,
                  "relation": Relation URI,
                  "distmetric: Distance measure for neighbour search (Optional,Default : Cosine)
              }
Sample request body:
{
    "indexname":"shallom_dbpedia_index",
    "relation" : "/resource/Boeing_747_hull_losses",
    "distmetric":"cosine"    
}
curl -X GET http://unikge.cs.upb.de:5001/get-relation-neighbour -H "Content-Type: application/json" -d '{"indexname":"shallom_dbpedia_index","relation" : "/resource/Boeing_747_hull_losses","distmetric":"cosine"}'


These APIs can be accessed from http://unikge.cs.upb.de:5001/ on UPB network for now.  
Data available in the indexes is documented in the [wiki](https://github.com/dice-group/kg-embedding-service/wiki/Indexes-unikge.cs.upb.de).  
A python implementation is available at [Universal_Embeddings: kg-embedding-service.py](https://github.com/dice-group/Universal_Embeddings/blob/main/kg-embedding-service.py), and a description in the [wiki](https://github.com/dice-group/Universal_Embeddings/wiki/KG-embedding-service).
