package schneider.thesis;

import org.graphstream.graph.implementations.SingleGraph;
/**
 * Graph Class inspired by
 * https://algorithms.tutorialhorizon.com/graph-implementation-adjacency-matrix-set-3/
 */
public class Graph {

  int vertexes;
  int[][] graph;
  int classLabel;

  /**
   * 
   * @param vertexes - size of the graph
   * @param classLabel - corresponding class inside the dataset
   */
  public Graph(int vertexes, int classLabel) {
    this.vertexes = vertexes;
    this.graph = new int[vertexes][vertexes];
    this.classLabel = classLabel;
  }

  /**
   * Add an edge to this graph
   * 
   * @param src - the index of the source node
   * @param dest - the index of the destination node
   * @return - this, the new Graph to chain operations
   */
  public Graph addEdge(int src, int dest) {
    this.graph[src][dest] = 1;
    this.graph[dest][src] = 1;

    return this;
  }

  /**
   * Remove an edge from this graph
   * 
   * @param src - the index of the source node
   * @param dest - the index of the destination node
   * @return - this, the new Graph to chain operations
   */
  public Graph removeEdge(int src, int dest) {
    this.graph[src][dest] = 0;
    this.graph[dest][src] = 0;

    return this;
  }

  public void display(String id) {
    SingleGraph graph = new SingleGraph(id);

    graph.addAttribute("ui.label", this.classLabel);
    for(int i = 0; i < this.graph.length; i++) {
      graph.addNode(String.valueOf(i));
    }
    for(int i = 0; i < this.graph.length; i++) {
      for(int j = 0; j < this.graph[i].length; j++) {
        if(graph.getEdge(i + "-" + j) == null) {
          if(this.graph[i][j] == 1) {
            graph.addEdge(j + "-" + i, String.valueOf(i), String.valueOf(j));
          }
        }
      }
    }
    graph.display();
  }
}
