## to test the location search of ES
## write several geo points to ES, then return the neighbors by distance order

from datetime import datetime
from pyelasticsearch.client import ElasticSearch

# by default we connect to localhost:9200
es = ElasticSearch('http://localhost:9200/')


mapping = {
	'user_geos': {
		'properties': {
			'uid': {'type': 'integer'},
			'location': {'type': 'geo_point'}
		}
	},
	 'photo_geos': {
		'properties': {
			'pid': {'type': 'integer'},
			'location': {'type': 'geo_point'}
		}
	}
}

## create index

try:
	es.delete_index('geos')
	print "Index 'geos' deleted!"
except Exception as e:
	pass
es.create_index('geos', settings={'mappings': mapping})
print "Index 'geos' created!"
es.refresh('geos')

## bulk index
documents = [
	{
		'uid': 201,
		"location" : {
 			"lat" : 41.12,
 			"lon" : -71.34
 		}
	},
	{
		'uid': 202,
		"location" : {
 			"lat" : 41.13,
 			"lon" : -71.35
 		}
	},
	{
		'uid': 203,
		"location" : {
 			"lat" : 42.12,
 			"lon" : -72.34
 		}
	},
	{
		'uid': 204,
		"location" : {
 			"lat" : 45.102,
 			"lon" : -75.304
 		}
	},
	{
		'uid': 205,
		"location" : {
 			"lat" : 51.22,
 			"lon" : -81.44
 		}
	},

	# ...
]
# es.bulk_index('geos', 'user_geos', documents) #,id_field='uid'

for doc in documents:
    es.index('geos', 'user_geos', doc)
print "All documents indexed successfully!"
es.refresh('geos')

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
# print es.get('geos', 'user_geos', 205)
res =  es.search(query, index='geos')
print res
for r in res['hits']['hits']:
	print (r['sort'], r['_id'], r['_source']['location']) 