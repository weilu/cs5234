FILE_NAME=$1

HDFS_PATH=/user/hduser/$1/

# MapReduce to count degree for each node
rm cache.temp

hadoop jar $HADOOP_STREAMING/hadoop-streaming-3.1.1.jar \
        -input $HDFS_PATH/graph.in \
        -output $HDFS_PATH/temp/graph.temp \
        -file degree_mapper.py \
        -file degree_reducer.py \
        -mapper "python3 degree_mapper.py" \
        -reducer "python3 degree_reducer.py" \
        -jobconf mapred.reduce.tasks=2

#hdfs dfs -getmerge $HDFS_PATH/temp/graph.temp ./graph.temp
