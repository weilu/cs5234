#!/usr/bin/env bash
set -xe

HADOOP_PREFIX=/usr/local/Cellar/hadoop/2.8.2/
STREAMING_JAR=$HADOOP_PREFIX/libexec/share/hadoop/tools/lib/hadoop-streaming-2.8.2.jar
HADOOP=$HADOOP_PREFIX/bin/hadoop

TEMP_OUT_PREFIX=temp_out
DEGREE_OUT_DIR=$TEMP_OUT_PREFIX/degree
THRESHOLD_OUT_DIR=$TEMP_OUT_PREFIX/threshold
INPUT_DIR=/data
OUTPUT_DIR=/out

$HADOOP dfs -rm -r -f $INPUT_DIR $OUTPUT_DIR $TEMP_OUT_PREFIX
$HADOOP dfs -mkdir -p $INPUT_DIR
$HADOOP dfs -put ..$INPUT_DIR/ca-GrQc_preprocessed.txt $INPUT_DIR/

$HADOOP jar $STREAMING_JAR \
  -files degree_mapper.py,degree_reducer.py \
  -mapper degree_mapper.py \
  -reducer degree_reducer.py \
  -input $INPUT_DIR/ca-GrQc_preprocessed.txt \
  -output $DEGREE_OUT_DIR
# $HADOOP dfs -cat $DEGREE_OUT_DIR/part-00000

$HADOOP jar $STREAMING_JAR \
  -files threshold_mapper.py,threshold_reducer.py \
  -mapper threshold_mapper.py \
  -reducer 'threshold_reducer.py 1' \
  -input $DEGREE_OUT_DIR \
  -output $THRESHOLD_OUT_DIR \
  -numReduceTasks 1
$HADOOP dfs -cat $THRESHOLD_OUT_DIR/part-00000

