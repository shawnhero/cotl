from pyelasticsearch.client import ElasticSearch
# by default we connect to localhost:9200
es = ElasticSearch('http://localhost:9200/')

query = {
	"from" : 0, "size" : 3,
	'query': {
		 "match_all" : { }
	 }
	 ,
	 "sort" : [
		{
			"_geo_distance" : {
				"location" : [41.12, -71.34],
				"order" : "desc",
				"unit" : "km"
			}
		}
	]

 }
query2 = {'sort': [{'_geo_distance': {'location': [37.41980952286528, -122.31275946636089], 'unit': 'km', 'order': 'asc'}}], 'query': {'match_all': {}}, 'from': 0, 'size': 10}
# print es.get('geos', 'user_geos', 205)
res =  es.search(query2, index='geos',doc_type=['user_geos'])
uids = [r['_source']['uid'] for r in res['hits']['hits']]
print len(uids)
print uids