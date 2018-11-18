FILE_NAME=$1

HDFS_TMP_PATH=/user/hduser/$1/temp

# MapReduce to count degree for each node
rm cache.temp
hdfs dfs -rm -r $HDFS_TMP_PATH/degree.temp

hadoop jar $HADOOP_STREAMING/hadoop-streaming-3.1.1.jar \
        -input $HDFS_TMP_PATH/graph.temp/ \
        -output $HDFS_TMP_PATH/degree.temp/ \
        -file degree_mapper.py \
        -file degree_reducer.py \
        -mapper "python3 degree_mapper.py" \
        -reducer "python3 degree_reducer.py" \
        -jobconf mapred.reduce.tasks=2

hdfs dfs -rm -r $HDFS_TMP_PATH/graph.temp
hdfs dfs -cp -f $HDFS_TMP_PATH/degree.temp $HDFS_TMP_PATH/graph.temp

hdfs dfs -getmerge $HDFS_TMP_PATH/graph.temp ./graph.temp
