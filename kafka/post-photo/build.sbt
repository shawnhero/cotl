// Project name (artifact name in Maven)
name := "kafka consumer"

// orgnization name (e.g., the package name of the project)
organization := "com.shawn-insight"

version := "1.0-SNAPSHOT"

// project description
description := "Shawn Data Project"

// Enables publishing to maven repo
publishMavenStyle := true

// Do not append Scala versions to the generated artifacts
crossPaths := false

// This forbids including Scala related libraries into the dependency
autoScalaLibrary := false

// library dependencies. (orginization name) % (project name) % (version)
libraryDependencies += "org.apache.kafka" % "kafka_2.10" % "0.8.2-beta"


