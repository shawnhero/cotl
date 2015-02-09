from pyelasticsearch.client import ElasticSearch
import sys
# by default we connect to localhost:9200


if __name__ == "__main__":
	if len(sys.argv)!=3:
		print "Usage: [*.py] [lat] [lon]"
		sys.exit(0)
	es = ElasticSearch('http://localhost:9200/')
	lat = float(sys.argv[1])
	lon = float(sys.argv[2])
	print lat, lon
	query = {
		"from" : 0, "size" : 10,
		'query': {
			 "match_all" : { }
		 },
		 "filter" : {
			"geo_distance" : {
				"distance" : "100km",
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
	res =  es.search(query1, index='photo_geos',doc_type=['photos'])
	print res
	uids = [(r['_id'],r['sort'], r['_source']['location']) for r in res['hits']['hits']]
	print len(uids)
	for i in range(len(uids)):
		print uids[i]