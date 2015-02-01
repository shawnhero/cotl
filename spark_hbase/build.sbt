name := "spark_hbase"

version := "1.0"

scalaVersion := "2.10.4"

libraryDependencies ++= Seq(
	"it.nerdammer.bigdata" % "spark-hbase-connector_2.10" % "0.9.2",
    "org.scalatest" % "scalatest_2.10" % "2.2.3" % "test",
	"org.apache.spark" % "spark-core_2.10" % "1.2.0",
	"org.apache.hbase" % "hbase-common" % "0.98.8-hadoop2",
	"org.apache.hbase" % "hbase-client" % "0.98.8-hadoop2",
	"org.apache.hbase" % "hbase-server" % "0.98.8-hadoop2"
)