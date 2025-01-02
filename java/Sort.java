import java.io.FileWriter;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;

public class Sort {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n-1; i++) {
            for (int j = 0; j < n-i-1; j++) {
                if (arr[j] > arr[j+1]) {
                    int temp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1] = temp;
                }
            }
        }
    }

    public static void main(String[] args) {
        int[] arr = {2493, 3089, 4076, 2354, 4385, /*... (your array data) ...*/};

        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        long startCpuTime = bean.getCurrentThreadCpuTime();
        long startTime = System.nanoTime();

        for (int i = 0; i < 1000; i++) {
            bubbleSort(arr);
        }

        long endCpuTime = bean.getCurrentThreadCpuTime();
        long endTime = System.nanoTime();

        try (FileWriter log = new FileWriter("log.txt")) {
            log.write("Execution time: " + (endTime - startTime) / 1e6 + " ms\n");
            log.write("CPU time: " + (endCpuTime - startCpuTime) / 1e6 + " ms\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
