package schneider.thesis;

import java.io.IOException;

public class Main {
  public static void main(String[] args) {
    GraphDataSet dataSet = new GraphDataSet("AIDS");
    try {
      dataSet.readFromFile();
    } catch (IOException e) {
      e.printStackTrace();
    }

    dataSet.displayGraph(934);
    dataSet.displayGraph(1323);
    dataSet.displayGraph(1210);
  }
}
