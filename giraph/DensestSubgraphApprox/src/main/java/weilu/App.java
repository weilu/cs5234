package weilu;

import org.apache.giraph.edge.Edge;
import org.apache.giraph.graph.BasicComputation;
import org.apache.giraph.graph.Vertex;
import org.apache.hadoop.io.*;
import org.apache.log4j.Logger;

import java.io.IOException;


// <Vertex id, Vertex data, Edge data, Message type>
public class App extends BasicComputation<IntWritable, IntWritable, NullWritable, IntWritable> {


  private static final Logger LOG = Logger.getLogger(App.class);

  @Override
  public void compute(
      Vertex<IntWritable, IntWritable, NullWritable> vertex,
      Iterable<IntWritable> messages) throws IOException {

    // only send remove vertex request when no pending vertexes & edges removals & MC sees the correct state of world
    if (getSuperstep() % 3 == 1) {
      double threshold = ((DoubleWritable) getAggregatedValue(DensityMasterCompute.DEGREE_THRESHOLD)).get();

      if (vertex.getNumEdges() <= threshold) {
        // remove self (actually happens at the beginning of next superstep)
        removeVertexRequest(vertex.getId());

        // according to the Pregel paper, "removing a vertex implicitly removes all of its out-edges"
        // send messages to neighbor to remove in-edges, make sure giraph.vertex.resolver.create.on.msgs=false
        sendMessageToAllEdges(vertex, vertex.getId());

        LOG.info("vertex " + vertex.getId() +
            " is to be removed because its degree " + vertex.getNumEdges() +
            " is less than " + threshold);
        aggregate(DensityMasterCompute.NUM_VERTEXES_TO_BE_REMOVED, new IntWritable(1));
      }
    }

    for (IntWritable message : messages) {
      vertex.removeEdges(message); // happens instantly as it's local removal
    }

    // No need to voteToHalt as the program terminates when all nodes are removed
  }
}


