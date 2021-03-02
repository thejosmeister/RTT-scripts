from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

body = {'query': {'bool': {'must': {'match': {'uid': 'uid1'}}}}}
list_of_source = es.search(body=body,index='testindex', filter_path=['hits.hits._source'])['hits']['hits']

[print(a['_source']) for a in list_of_source]


# body = {
#     "query" : {
#         "terms" : {
#             "TT" : {
#                 "index" : "testindex",
#                 "type" : "TT",
#                 "id": "uid1",
#                 "path" : "locations"
#             }
#         }
#     }
# }
#
#
#
# list_of_source = es.search(body=body, index='testindex', filter_path=['hits.hits._source'])['hits']['hits']
#
# [print(a['_source']) for a in list_of_source]
