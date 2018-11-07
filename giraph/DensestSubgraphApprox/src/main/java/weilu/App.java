package weilu;

import org.apache.giraph.graph.BasicComputation;
import org.apache.giraph.graph.Vertex;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.log4j.Logger;

import java.io.IOException;


// <Vertex id, Vertex data, Edge data, Message type>
public class App extends BasicComputation<IntWritable, IntWritable, NullWritable, IntWritable> {

  public static final double epsilon = 0.001;
  private static final Logger LOG = Logger.getLogger(App.class);

  @Override
  public void compute(
      Vertex<IntWritable, IntWritable, NullWritable> vertex,
      Iterable<IntWritable> messages) throws IOException {

    long threshold = Math.round(2 * (1 + epsilon) * getTotalNumEdges() / getTotalNumVertices());

    if (vertex.getNumEdges() <= threshold) {
      sendMessageToAllEdges(vertex, vertex.getId()); // if no vertex is removed then no more message is sent
      removeVertexRequest(vertex.getId());
      LOG.info("vertex " + vertex.getId() +
          " is to be removed because its degree " + vertex.getNumEdges() +
          " is less than " + threshold);
    } else {
      int numEdgesToRemove = 0;
      for (IntWritable message : messages) {
        // according to the Pregel paper, "removing a vertex implicitly removes all of its out-edges"
        removeEdgesRequest(vertex.getId(), new IntWritable(message.get()));
        numEdgesToRemove++;
      }
      LOG.info("vertex " + vertex.getId() +
          " not removed, because it has degree " + vertex.getNumEdges() +
          " It has following incoming edges to be removed: " + numEdgesToRemove);
    }

    // No need to voteToHalt as the program terminates when all nodes are removed
  }
}


