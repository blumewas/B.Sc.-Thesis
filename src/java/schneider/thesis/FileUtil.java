package schneider.thesis;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

public class FileUtil {

  /**
   * Helps us to count the lines in a given file
   * 
   * @param file - the file to count the lines in
   * @return the number of lines, returns 0 if no chars can be read
   * @throws IOException
   * 
   * @reference https://stackoverflow.com/a/453067/8529004
   */
  public static int countLines(File file) throws IOException {
    InputStream is = new BufferedInputStream(new FileInputStream(file));
    try {
      byte[] c = new byte[1024];

      int readChars = is.read(c);
      if (readChars == -1) {
        // bail out if nothing to read
        return 0;
      }

      // make it easy for the optimizer to tune this loop
      int count = 0;
      while (readChars == 1024) {
        for (int i = 0; i < 1024;) {
          if (c[i++] == '\n') {
            ++count;
          }
        }
        readChars = is.read(c);
      }

      // count remaining characters
      while (readChars != -1) {
        System.out.println(readChars);
        for (int i = 0; i < readChars; ++i) {
          if (c[i] == '\n') {
            ++count;
          }
        }
        readChars = is.read(c);
      }

      return count == 0 ? 1 : count;
    } finally {
      is.close();
    }
  }
}
