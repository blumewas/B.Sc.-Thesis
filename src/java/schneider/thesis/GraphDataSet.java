package schneider.thesis;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class GraphDataSet {

  String name;
  ArrayList<Graph> graphs;
  // value that is true, if a DataSet is fully created from the files
  boolean initialized = false;

  private final String path;

  /**
   * Initialise a DataSet of Graphs using the name of the Graph
   * @param name - the name of the DataSet
   */
  public GraphDataSet(String name) {
    this.name = name;
    this.graphs = new ArrayList<Graph>();

    this.path = System.getProperty("user.dir") + "/../Graphs/" + name + "/";
  }

  /**
   * Initialise the DataSet using the files
   * @throws IOException
   */
  public void readFromFile() throws IOException {
    this.initialized = false;
    System.out.println("Reading DataSet: " + name);

    // Edges
    File file_A = new File(this.path + name + "_A.txt");
    // Graph to label relation
    File file_graph_labels = new File(this.path + name + "_graph_labels.txt");
    // Node to Graph relation
    File file_graph_indicator = new File(this.path + name + "_graph_indicator.txt");

    int graphCount = FileUtil.countLines(file_graph_labels);

    BufferedReader readerIndicator = new BufferedReader(new FileReader(file_graph_indicator));
    BufferedReader readerA = new BufferedReader(new FileReader(file_A));

    String lastIndicator = null;
    String lastEdge = null;

    for (int i = 0; i < graphCount; i++) {
      int label = this.getLabelForGraph(i);

      int graphNumber = i + 1;
      // Number of Vertexes in Graph
      int vertexCount = 0;

      // Save the Nodes that belong to this Graph
      ArrayList<String> nodes = new ArrayList<String>();
      
      // The number of the Node
      String indicator;
      // Work around so we wont skip any lines because the reader cant go back
      if(lastIndicator == null){
        indicator = readerIndicator.readLine();
      } else {
        indicator = lastIndicator;
      }

      // Count the number of Vertexes
      while(indicator != null) {
        int dataInt = Integer.valueOf(indicator);

        if(graphNumber < dataInt) {
          // We encountered a new Graph Number
          break;
        }
        vertexCount++;
        nodes.add(indicator);

        indicator = readerIndicator.readLine();
      }
      
      Graph graph = new Graph(vertexCount, label);

      // current edge
      String edge;
      // Work around so we wont skip any lines because the reader cant go back
      if(lastEdge == null) {
        edge = readerA.readLine();
      } else { 
        edge = lastEdge;
      }
      
      // Add all edges until we encounter one, that is between two nodes that are not in the current graph
      while(edge != null) {
        String[] srcDest = edge.split(",");
        if(!nodes.contains(srcDest[0])) {
          break;
        }
        // add the edge, strip of all whitespaces we may encounter
        graph.addEdge(Integer.valueOf(srcDest[0].replaceAll("\\s+","")), Integer.valueOf(srcDest[1].replaceAll("\\s+","")));
        edge = readerA.readLine();
      }

      this.graphs.add(graph);
    }
    readerIndicator.close();
    readerA.close();

    this.initialized = true;
  }

  /**
   * 
   * @return - the size of the DataSet
   */
  public int size() {
    return this.graphs.size();
  }

  /**
   * 
   * @param index - index of Graph in the DataSet
   * @throws IOException
   */
  private int getLabelForGraph(int index) throws IOException {
    if(this.graphs.size() > index) { // Check if we already have the Graph in the DataSet
      return this.graphs.get(index).classLabel;
    } else {
      // Otherwise we need to read lines, until we are at the corresponding line
      File file_graph_labels = new File(this.path + name + "_graph_labels.txt");
      BufferedReader reader = new BufferedReader(new FileReader(file_graph_labels));
      for(int i = 0; i < index; i++) {
        reader.readLine();
      }
      int label = Integer.valueOf(reader.readLine());
      reader.close();
      return label;
    }
  }

}
