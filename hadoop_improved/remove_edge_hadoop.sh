FILE_NAME=$1
T=$2

HDFS_TMP_PATH=/user/hduser/$1/temp

# Prepare to remove edges
rm cache.temp
hdfs dfs -rm -r $HDFS_TMP_PATH/graph/

hadoop jar $HADOOP_STREAMING/hadoop-streaming-3.1.1.jar \
        -input $HDFS_TMP_PATH/graph.temp/ \
        -output $HDFS_TMP_PATH/graph/ \
        -file remove_edge_second_mapper.py \
        -file remove_edge_second_reducer.py \
        -mapper "python3 remove_edge_second_mapper.py "$T \
        -reducer "python3 remove_edge_second_reducer.py" \
		-jobconf stream.num.map.output.key.fields=1 \
		-jobconf num.key.fields.for.partition=2 \
        -jobconf mapred.reduce.tasks=2

#hdfs dfs -getmerge $HDFS_TMP_PATH/graph/ ./graph_second.temp
hdfs dfs -rm -r $HDFS_TMP_PATH/graph.temp/

hadoop jar $HADOOP_STREAMING/hadoop-streaming-3.1.1.jar \
        -input $HDFS_TMP_PATH/graph/ \
        -output $HDFS_TMP_PATH/graph.temp/ \
        -file remove_edge_first_mapper.py \
        -file remove_edge_first_reducer.py \
        -mapper "python3 remove_edge_first_mapper.py " \
        -reducer "python3 remove_edge_first_reducer.py" \
        -jobconf mapred.reduce.tasks=2

#hdfs dfs -getmerge $HDFS_TMP_PATH/graph.temp/ ./graph_first.temp
