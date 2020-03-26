package schneider.thesis;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class GraphDataSet {

  String name;
  ArrayList<Graph> graphs;
  boolean initialized = false;

  private final String path;

  public GraphDataSet(String name) {
    this.name = name;
    this.graphs = new ArrayList<Graph>();

    this.path = System.getProperty("user.dir") + "/../Graphs/" + name + "/";
  }

  public void readFromFile() throws IOException {
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
      int vertexCount = 0;

      // Look which Nodes belong to this Graph
      ArrayList<String> nodes = new ArrayList<String>();
      String indicator;
      
      if(lastIndicator == null){
        indicator = readerIndicator.readLine();
      } else {
        indicator = lastIndicator;
      }

      while(indicator != null) {
        int dataInt = Integer.valueOf(indicator);
        
        if(graphNumber < dataInt) {
          break;
        }
        vertexCount++;
        nodes.add(indicator);

        indicator = readerIndicator.readLine();
      }
      System.out.println(graphNumber);
      System.out.println(vertexCount);
      Graph graph = new Graph(vertexCount, label);

      String edge;
      if(lastEdge == null) {
        edge = readerA.readLine();
      } else { 
        edge = lastEdge;
      }
      
      while(edge != null) {
        String[] srcDest = edge.split(",");
        if(!nodes.contains(srcDest[0])) {
          break;
        }
        graph.addEdge(Integer.valueOf(srcDest[0].replaceAll("\\s+","")), Integer.valueOf(srcDest[1].replaceAll("\\s+","")));
        edge = readerA.readLine();
      }

      this.graphs.add(graph);
    }
    readerIndicator.close();
    readerA.close();

    this.initialized = true;
  }

  public int size() {
    return this.graphs.size();
  }

  /**
   * 
   * @param index - index of Graph in the DataSet
   * @throws IOException
   */
  private int getLabelForGraph(int index) throws IOException {
    if(this.graphs.size() > index) {
      return this.graphs.get(index).classLabel;
    } else {
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
