from datetime import datetime
from pyelasticsearch.client import ElasticSearch

# by default we connect to localhost:9200
es = ElasticSearch('http://localhost:9200/')


entry_mapping = {
    'entry_type': {
        'properties': {
            'uid': {'type': 'integer'},
            'location': {'type': 'geo_point'}
        }
    }
}

## create index

try:
	es.delete_index('user_geo_index')
	print "Index 'user_geo_index' deleted!"
except Exception as e:
	pass
es.create_index('user_geo_index', settings={'mappings': entry_mapping})
print "Index 'user_geo_index' created!"
es.refresh('user_geo_index')

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
es.bulk_index('user_geo_index', 'entry_type', documents, id_field='uid')
print "All documents indexed successfully!"
es.refresh('user_geo_index')

query = {
	"from" : 0, "size" : 3,
	'query': {
         # 'filtered': {
         #     'filter': {
         #      "geo_distance" : {
         #        "distance" : "1102km",
         #        "location" : {
         #            "lat" : 41.12,
         #            "lon" : -71.34
         #        }
         #    }
         #     },
         # },
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
# print es.get('user_geo_index', 'entry_type', 205)
res =  es.search(query, index='user_geo_index')
for r in res['hits']['hits']:
	print (r['sort'], r['_id'], r['_source']['location']) 