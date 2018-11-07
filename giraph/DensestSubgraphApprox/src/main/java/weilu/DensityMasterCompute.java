package weilu;

import org.apache.giraph.aggregators.DoubleMaxAggregator;
import org.apache.giraph.master.DefaultMasterCompute;
import org.apache.hadoop.io.DoubleWritable;

public class DensityMasterCompute extends DefaultMasterCompute {
  public static final String MAX_DENSITY = "MaxDensityAggregator";


  @Override
  public void compute() {
    if (getTotalNumVertices() == 0) {
      return;
    }

    // only nodes & their out-edges are removed at this stage, there are dangling in-edges to be removed still
    if (getSuperstep() % 2 == 0) {
      return;
    }

    System.out.println("At superstep " + getSuperstep() +
        ", number of edges: " + getTotalNumEdges() + ", number of vertexes: " + getTotalNumVertices());

    double maxDensity = ((DoubleWritable) getAggregatedValue(MAX_DENSITY)).get();
    double currDensity = 1.0 * getTotalNumEdges() / getTotalNumVertices() / 2; // Undirected graph therefore / 2
    // TODO: update to new subgraph with higher density
    if (maxDensity < currDensity) {
      setAggregatedValue(MAX_DENSITY, new DoubleWritable(currDensity));
      System.out.println("Max density at superstep " + getSuperstep() +
          " is updated from " + maxDensity + " to " + currDensity);
    }
  }

  @Override
  public void initialize() throws InstantiationException, IllegalAccessException {
    registerPersistentAggregator(MAX_DENSITY, DoubleMaxAggregator.class);
  }
}
