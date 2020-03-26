package schneider.thesis;

import java.io.IOException;

public class Main {
  public static void main(String[] args) {
    GraphDataSet dataSet = new GraphDataSet("NCI1");
    try {
      dataSet.readFromFile();
    } catch (IOException e) {
      e.printStackTrace();
    }
    System.out.println(dataSet.initialized);
  }
}
