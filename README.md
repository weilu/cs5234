# Densest Subgraph Algorithms

Code repo for CS5234 Combinatorial and Graph Algorithms mini-project.

## Development

### Data Preprocessing

Undirected graph network data comes from https://snap.stanford.edu/data/.
The data comes in edge pairs, one pair per line separated by tab,
with duplicates such as 1 2 and 2 1. However duplicates don't always exists,
so we clean up the data by preprocessing it and removing such duplicates and
comment lines that starts with #.

```
# produces data/*_preprocessed.txt files
python preprocess.py
```

### Baseline Algorithm

Exact min-cut based algorithm by [Goldberg](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1984/CSD-84-171.pdf) implemented in python.

Setup:

```
# If not MacOS, see https://git.skewed.de/count0/graph-tool/wikis/installation-instructions
brew install graph-tool

# virtualenv needs to be created with --system-site-packages to access graph-tool
mkvirtualenv --python=`which python3` --system-site-packages cs5234
```

Run:

```
python densest_subgraph_goldberg.py
```

### Distributed Algorithm

2-approximate algorithm by [Bahmani, Kumar and Vassilvitskii](http://vldb.org/pvldb/vol5/p454_bahmanbahmani_vldb2012.pdf) implemented in Giraph using Java.

Setup: http://giraph.apache.org/quick_start.html

Run:

```
cd giraph/DensestSubgraphApprox/

# make jar
mvn clean compile assembly:single

# upload test data to hdfs
$HADOOP_HOME/bin/hadoop dfs -mkdir -p /user/giraph/input/
$HADOOP_HOME/bin/hadoop dfs -copyFromLocal ../../data/*_preprocessed.txt /user/giraph/input/

# run job, change path accordingly
export HADOOP_CLASSPATH=/usr/local/giraph/giraph-core/target/giraph-1.3.0-SNAPSHOT-for-hadoop-2.8.2-jar-with-dependencies.jar:/Users/luwei/workspace/CS5234/cs5234_project/giraph/DensestSubgraphApprox/target/DensestSubgraphApprox-1.0-SNAPSHOT-jar-with-dependencies.jar
export LIBJARS=/usr/local/giraph/giraph-core/target/giraph-1.3.0-SNAPSHOT-for-hadoop-2.8.2-jar-with-dependencies.jar,/Users/luwei/workspace/CS5234/cs5234_project/giraph/DensestSubgraphApprox/target/DensestSubgraphApprox-1.0-SNAPSHOT-jar-with-dependencies.jar
hadoop jar /usr/local/giraph/giraph-core/target/giraph-1.3.0-SNAPSHOT-for-hadoop-2.8.2-jar-with-dependencies.jar \
  org.apache.giraph.GiraphRunner -libjars ${LIBJARS} weilu.App \
  -mc weilu.DensityMasterCompute -aw org.apache.giraph.aggregators.TextAggregatorWriter \
  -ca giraph.textAggregatorWriter.frequency=1 \
  -ca giraph.vertex.resolver.create.on.msgs=false \
  -ca giraph.logLevel=trace \
  -eif org.apache.giraph.io.formats.IntNullReverseTextEdgeInputFormat \
  -eip /user/giraph/input/ca-GrQc_preprocessed.txt -w 1

# see results
$HADOOP_HOME/bin/hadoop dfs -cat /user/giraph/aggregatorValues_0
```
