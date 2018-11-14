#!/usr/bin/env bash
set -xe

HADOOP_PREFIX=/usr/local/Cellar/hadoop/2.8.2/
STREAMING_JAR=$HADOOP_PREFIX/libexec/share/hadoop/tools/lib/hadoop-streaming-2.8.2.jar
HADOOP=$HADOOP_PREFIX/bin/hadoop

TEMP_OUT_PREFIX=temp_out
DEGREE_OUT_DIR=$TEMP_OUT_PREFIX/degree
THRESHOLD_OUT_DIR=$TEMP_OUT_PREFIX/threshold
VERTEX_REMOVED_OUT_DIR=$TEMP_OUT_PREFIX/vertex_removed
EDGE_REMOVED_OUT_DIR=$TEMP_OUT_PREFIX/edge_removed
INPUT_DIR=/data
INPUT_FILE=ca-GrQc_preprocessed.txt
OUTPUT_DIR=/out

$HADOOP dfs -rm -r -f $INPUT_DIR $OUTPUT_DIR $TEMP_OUT_PREFIX
$HADOOP dfs -mkdir -p $INPUT_DIR
$HADOOP dfs -put ..$INPUT_DIR/$INPUT_FILE $INPUT_DIR/

$HADOOP jar $STREAMING_JAR \
  -files degree_mapper.py,degree_reducer.py \
  -mapper degree_mapper.py \
  -reducer degree_reducer.py \
  -input $INPUT_DIR/$INPUT_FILE \
  -output $DEGREE_OUT_DIR
# $HADOOP dfs -cat $DEGREE_OUT_DIR/part-00000

$HADOOP jar $STREAMING_JAR \
  -files threshold_mapper.py,threshold_reducer.py \
  -mapper threshold_mapper.py \
  -reducer 'threshold_reducer.py 1' \
  -input $DEGREE_OUT_DIR \
  -output $THRESHOLD_OUT_DIR \
  -numReduceTasks 1

# {m n threshold density}
read M N THRESHOLD DENSITY <<< $($HADOOP dfs -cat $THRESHOLD_OUT_DIR/part-00000)
echo "edges: $M, nodes: $N, threshold: $THRESHOLD, density: $DENSITY"
MAX_DENSITY=$DENSITY

while [[ ! -z "$N" && $N -gt 0 ]]
do
  # sort by both fields
  $HADOOP jar $STREAMING_JAR \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -files removal_mapper.py,removal_reducer.py \
    -mapper "removal_mapper.py $THRESHOLD" \
    -reducer removal_reducer.py \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -input $DEGREE_OUT_DIR \
    -output $VERTEX_REMOVED_OUT_DIR

  $HADOOP dfs -rm -r -f $OUTPUT_DIR

  # sort by all 3 fields
  $HADOOP jar $STREAMING_JAR \
    -D stream.num.map.output.key.fields=3 \
    -D num.key.fields.for.partition=1 \
    -files edge_removal_reducer.py \
    -mapper cat \
    -reducer edge_removal_reducer.py \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -input $VERTEX_REMOVED_OUT_DIR \
    -output $OUTPUT_DIR

  $HADOOP dfs -rm -r -f $TEMP_OUT_PREFIX

  # no need to use degree mapper as the edges have already been doubled
  $HADOOP jar $STREAMING_JAR \
    -files degree_reducer.py \
    -mapper cat \
    -reducer degree_reducer.py \
    -input $OUTPUT_DIR \
    -output $DEGREE_OUT_DIR
  # $HADOOP dfs -cat $DEGREE_OUT_DIR/part-00000

  $HADOOP jar $STREAMING_JAR \
    -files threshold_mapper.py,threshold_reducer.py \
    -mapper threshold_mapper.py \
    -reducer 'threshold_reducer.py 1' \
    -input $DEGREE_OUT_DIR \
    -output $THRESHOLD_OUT_DIR \
    -numReduceTasks 1

  read M N THRESHOLD DENSITY <<< $($HADOOP dfs -cat $THRESHOLD_OUT_DIR/part-00000)
  echo "edges: $M, nodes: $N, threshold: $THRESHOLD, density: $DENSITY"

  if [[ ! -z "$DENSITY" && $(echo "$DENSITY>$MAX_DENSITY" | bc ) -eq 1 ]]
  then
    MAX_DENSITY=$DENSITY
    echo "updating MAX_DENSITY = $MAX_DENSITY"
  fi
done

echo "$INPUT_FILE densest subgraph density: $MAX_DENSITY"
