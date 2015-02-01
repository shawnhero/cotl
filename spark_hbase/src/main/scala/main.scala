import it.nerdammer.spark.hbase._
import org.apache.spark.SparkConf

import org.apache.spark._


object HelloWorld {
	def main(args: Array[String]) {
		println("Hello, world!")
		val sparkConf = new SparkConf()
		sparkConf.set("spark.hbase.host", "c0tl.com").setMaster("local").setAppName("shawnhero")
		sparkConf.setSparkHome("/opt/cloudera/parcels/CDH-5.3.0-1.cdh5.3.0.p0.30/lib/spark")
		val sc = new SparkContext(sparkConf)


		val rdd = sc.parallelize(1 to 100)
						.map(i => (i.toString, i+1, "Hello"))

		// rdd.toHBaseTable("t1")
		// 	 .toColumns("number", "word")
		// 	 .inColumnFamily("f1")
		// 	 .save()

		// read from HBase
		val hBaseRDD = sc.hbaseTable[(Int,Int, Int)]("photos")
			.select("born_lat", "born_lon")
			.inColumnFamily("details")
		hBaseRDD.foreach(println)
  }
}



// val hBaseRDD = sc.hbaseTable[(String, Int, String)]("mytable")
//	  .select("column1", "column2")
//	  .inColumnFamily("mycf")