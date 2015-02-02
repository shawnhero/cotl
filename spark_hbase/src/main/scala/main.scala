import org.apache.spark.SparkConf

import org.apache.spark._


object HelloWorld {
	def main(args: Array[String]) {
		// Nothing to see here just creating a SparkContext like you normally would

		val sparkConf = new SparkConf()
		sparkConf.set("spark.hbase.host", "c0tl.com").setMaster("local").setAppName("shawnhero")
		sparkConf.setSparkHome("/opt/cloudera/parcels/CDH-5.3.0-1.cdh5.3.0.p0.30/lib/spark")
		val sc = new SparkContext(sparkConf)

		val columnFamily = "metrics"
		//This is making a RDD of
		//(RowKey, columnFamily, columnQualifier, value)
		val rdd = sc.parallelize(Array(
				(Bytes.toBytes("1"), Array((Bytes.toBytes(columnFamily), Bytes.toBytes("1"), Bytes.toBytes("1")))),
				(Bytes.toBytes("2"), Array((Bytes.toBytes(columnFamily), Bytes.toBytes("1"), Bytes.toBytes("2")))),
				(Bytes.toBytes("3"), Array((Bytes.toBytes(columnFamily), Bytes.toBytes("1"), Bytes.toBytes("3")))),
				(Bytes.toBytes("4"), Array((Bytes.toBytes(columnFamily), Bytes.toBytes("1"), Bytes.toBytes("4")))),
				(Bytes.toBytes("5"), Array((Bytes.toBytes(columnFamily), Bytes.toBytes("1"), Bytes.toBytes("5"))))
			 )
			)
		 
		//Create the HBase config like you normally would then
		//Pass the HBase configs and SparkContext to the HBaseContext
		val conf = HBaseConfiguration.create();
			conf.addResource(new Path("/etc/hbase/conf/core-site.xml"));
			conf.addResource(new Path("/etc/hbase/conf/hbase-site.xml"));
		val hbaseContext = new HBaseContext(sc, conf);
		 
		//Now give the rdd, table name, and a function that will convert a RDD record to a put, and finally
		// A flag if you want the puts to be batched
		hbaseContext.bulkPut[(Array[Byte], Array[(Array[Byte], Array[Byte], Array[Byte])])](rdd,
			"photos_tmp",
			//This function is really important because it allows our source RDD to have data of any type
			// Also because puts are not serializable
			(putRecord) > {
				val put = new Put(putRecord._1)
				putRecord._2.foreach((putValue) > put.add(putValue._1, putValue._2, putValue._3))
				 put
			},
			true);







		// val rdd = sc.parallelize(1 to 5)
	//			 .map(i => (i.toString,	"Hello, world", i+1, i+2))

		// rdd.toHBaseTable("t1")
		// 	 .toColumns("number", "word")
		// 	 .inColumnFamily("f1")
		// 	 .save()

		// read from HBase
		// val hBaseRDD = sc.hbaseTable[(String,String, Int, Int)]("photos_sub")
		// 	.select("tags","born_lat", "born_lon")
		// 	.inColumnFamily("details")
		// hBaseRDD.foreach(println)

		// val rdd = sc.parallelize(hBaseRDD.sc)
		// rdd.foreach(println)

		// hBaseRDD.toHBaseTable("photos_tmp")
		// 	 .toColumns("tags", "born_lat","born_lon")
		// 	 .inColumnFamily("details")
		// 	 .save()

	}
}



// val hBaseRDD = sc.hbaseTable[(String, Int, String)]("mytable")
//		.select("column1", "column2")
//		.inColumnFamily("mycf")







