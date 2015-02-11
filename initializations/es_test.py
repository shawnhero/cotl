from pyelasticsearch.client import ElasticSearch
import sys
# by default we connect to localhost:9200


if __name__ == "__main__":
	if len(sys.argv)!=4:
		print "Usage: [*.py] [lat] [lon] [R]"
		sys.exit(0)
	es = ElasticSearch('http://localhost:9200/')
	lat = float(sys.argv[1])
	lon = float(sys.argv[2])
	r = float(sys.argv[3])
	print lat, lon, r
	query = {
		"from" : 0, "size" : 10,
		'query': {
			 "match_all" : { }
		 },
		 "filter" : {
			"geo_distance" : {
				"distance" : str(r)+'km',
				"location" : {
					"lat" : lat,
					"lon" : lon
				}
			}
		},
		 "sort" : [
			{
				"_geo_distance" : {
					"location" :  {
						"lat" : lat,
						"lon" : lon
					},
					"order" : "asc",
					"unit" : "km"
				}
			}
		]

	 }
	query1 = {
		"from" : 0, "size" : 10,
		'query': {
			 "match_all" : { }
		 },
		"sort" : [
		{ "likes" : {"order" : "desc"}},
		"_score"
		],
	 }
	query_count = {
	 	"facets": {
        "count_by_type": {
            "terms": {
                "field": "_type"
            }
        }
    }
	 }
	# res =  es.search(query, index='photo_geos',doc_type=['photos'])
	res =  es.search(query_count, index='geos',doc_type=['user_geos'])
	print res
	sys.exit(0)


	uids = [(r['_id'],r['sort'][0], r['_source']['views'], r['_source']['likes'], r['_source']['location']['lat'], r['_source']['location']['lon']) for r in res['hits']['hits']]
	print len(uids)
	for i in range(len(uids)):
		print uids[i]