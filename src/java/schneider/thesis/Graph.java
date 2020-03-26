package schneider.thesis;

/**
 * Graph Class inspired by
 * https://algorithms.tutorialhorizon.com/graph-implementation-adjacency-matrix-set-3/
 */
public class Graph {

  int vertexes;
  int[][] graph;
  int classLabel;

  public Graph(int vertexes, int classLabel) {
    this.vertexes = vertexes;
    this.graph = new int[vertexes][vertexes];
    this.classLabel = classLabel;
  }

  public Graph addEdge(int src, int dest) {
    this.graph[src][dest] = 1;
    this.graph[dest][src] = 1;

    return this;
  }

  public Graph removeEdge(int src, int dest) {
    this.graph[src][dest] = 0;
    this.graph[dest][src] = 0;

    return this;
  }
}
