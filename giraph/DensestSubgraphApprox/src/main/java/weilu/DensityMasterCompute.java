package weilu;

import org.apache.giraph.aggregators.DoubleMaxAggregator;
import org.apache.giraph.aggregators.IntSumAggregator;
import org.apache.giraph.conf.FloatConfOption;
import org.apache.giraph.master.DefaultMasterCompute;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;

public class DensityMasterCompute extends DefaultMasterCompute {
  public static final String DEGREE_THRESHOLD  = "DegreeThresholdAggregator";
  public static final String MAX_DENSITY = "MaxDensityAggregator";
  public static final String NUM_VERTEXES_TO_BE_REMOVED = "VertexesToRemoveAggregator";

  public static final FloatConfOption EPSILON =
      new FloatConfOption("DensityMasterCompute.epsilon", 0.001f,
          "Approximation parameter epsilon");

  @Override
  public void compute() {
    if (getTotalNumVertices() == 0) {
      return;
    }

    // undirected graph, therefore divide by 2
    double currDensity = 0.5 * getTotalNumEdges() / getTotalNumVertices();
    double threshold = 2 * (1 + EPSILON.get(getConf())) * currDensity;
    setAggregatedValue(DEGREE_THRESHOLD, new DoubleWritable(threshold));

    double maxDensity = ((DoubleWritable) getAggregatedValue(MAX_DENSITY)).get();
    // TODO: update to new subgraph with higher density
    if (maxDensity < currDensity) {
      setAggregatedValue(MAX_DENSITY, new DoubleWritable(currDensity));
      System.out.println("Max density at superstep " + getSuperstep() +
          " is updated from " + maxDensity + " to " + currDensity);
    }

    System.out.println("At superstep " + getSuperstep() +
        ", threshold: " + threshold +
        ", currDensity: " + currDensity +
        ", number of edges: " + getTotalNumEdges() +
        ", number of vertexes: " + getTotalNumVertices() +
        ", number of vertexes to be removed: " + ((IntWritable) getAggregatedValue(NUM_VERTEXES_TO_BE_REMOVED)).get()
    );
  }

  @Override
  public void initialize() throws InstantiationException, IllegalAccessException {
    registerPersistentAggregator(DEGREE_THRESHOLD, DoubleMaxAggregator.class);
    registerPersistentAggregator(MAX_DENSITY, DoubleMaxAggregator.class);
    registerAggregator(NUM_VERTEXES_TO_BE_REMOVED, IntSumAggregator.class);
  }
}
