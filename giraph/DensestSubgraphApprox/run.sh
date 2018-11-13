#!/usr/bin/env bash
set -xe

# mvn clean compile assembly:single

# Prepare environment
export HADOOP_CLASSPATH=/usr/local/giraph/giraph-core/target/giraph-1.3.0-SNAPSHOT-for-hadoop-2.8.2-jar-with-dependencies.jar:/Users/luwei/workspace/CS5234/cs5234_project/giraph/DensestSubgraphApprox/target/DensestSubgraphApprox-1.0-SNAPSHOT-jar-with-dependencies.jar
export LIBJARS=/usr/local/giraph/giraph-core/target/giraph-1.3.0-SNAPSHOT-for-hadoop-2.8.2-jar-with-dependencies.jar,/Users/luwei/workspace/CS5234/cs5234_project/giraph/DensestSubgraphApprox/target/DensestSubgraphApprox-1.0-SNAPSHOT-jar-with-dependencies.jar

# Upload data files to hdfs
# $HADOOP_HOME/bin/hadoop dfs -mkdir -p /user/luwei/input/
# $HADOOP_HOME/bin/hadoop dfs -put -f ../../data/*_preprocessed.txt /user/luwei/input/

for file in ../../data/*_preprocessed.txt
do
  filename=${file##*/}
  for epsilon in 0.001 0.1 1
  do
    echo "Processing $filename with epsilon $epsilon"
    hadoop jar /usr/local/giraph/giraph-core/target/giraph-1.3.0-SNAPSHOT-for-hadoop-2.8.2-jar-with-dependencies.jar org.apache.giraph.GiraphRunner -libjars ${LIBJARS} weilu.App \
      -mc weilu.DensityMasterCompute \
      -aw org.apache.giraph.aggregators.TextAggregatorWriter \
      -ca giraph.textAggregatorWriter.frequency=-1 \
      -ca giraph.textAggregatorWriter.filename=out-$filename-$epsilon \
      -ca giraph.vertex.resolver.create.on.msgs=false \
      -ca DensityMasterCompute.epsilon=$epsilon \
      -eif org.apache.giraph.io.formats.IntNullReverseTextEdgeInputFormat \
      -eip /user/luwei/input/$filename \
      -w 1;
  done
done

