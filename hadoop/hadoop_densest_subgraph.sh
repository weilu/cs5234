FILE_NAME=$1
EPSILON=$2

HDFS_TMP_PATH=/user/hduser/$1.temp

# MapReduce to count degree for each node
rm cache.temp
rm degree.temp
hdfs dfs -rm -r $HDFS_TMP_PATH/degree/

hadoop jar $HADOOP_STREAMING/hadoop-streaming-3.1.1.jar \
        -input $HDFS_TMP_PATH/graph.temp \
        -output $HDFS_TMP_PATH/degree \
        -file degree_mapper.py \
        -file degree_reducer.py \
        -mapper "python3 degree_mapper.py" \
        -reducer "python3 degree_reducer.py" \
        -jobconf mapred.reduce.tasks=1

hdfs dfs -cp -f $HDFS_TMP_PATH/degree/part-00000 $HDFS_TMP_PATH/degree.temp
hdfs dfs -get $HDFS_TMP_PATH/degree.temp ./

# Put local cache file to HDFS (n, m)
echo 'epsilon\t'$EPSILON >> cache.temp

# Prepare to remove edges
hdfs dfs -rm -r $HDFS_TMP_PATH/graph

hadoop jar $HADOOP_STREAMING/hadoop-streaming-3.1.1.jar \
        -input $HDFS_TMP_PATH/graph.temp \
        -output $HDFS_TMP_PATH/graph \
        -file cache.temp \
        -file degree.temp \
        -file remove_edge_mapper.py \
        -file remove_edge_reducer.py \
        -mapper "python3 remove_edge_mapper.py" \
        -reducer "python3 remove_edge_reducer.py" \
        -jobconf mapred.reduce.tasks=1

hdfs dfs -cp -f $HDFS_TMP_PATH/graph/part-00000 $HDFS_TMP_PATH/graph.temp

