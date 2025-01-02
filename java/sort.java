import java.io.FileWriter;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryUsage;
import com.sun.management.OperatingSystemMXBean;
import java.util.Arrays;
import java.util.Collections;
public class sort {
    public static void main(String[] args) throws IOException {
        int size = 1_000_000;
        Integer[] arr = new Integer[size];
        for (int i = 0; i < size; i++) {
            arr[i] = i + 1;
        }
        MemoryMXBean memoryMXBean = ManagementFactory.getMemoryMXBean();
        MemoryUsage beforeUsage = memoryMXBean.getHeapMemoryUsage();
        long usedMemoryBefore = beforeUsage.getUsed();
        OperatingSystemMXBean osBean = (OperatingSystemMXBean) ManagementFactory.getOperatingSystemMXBean();
        long startCpuTime = osBean.getProcessCpuTime();
        long startTime = System.nanoTime();
        Arrays.sort(arr, Collections.reverseOrder());
        long endTime = System.nanoTime();
        MemoryUsage afterUsage = memoryMXBean.getHeapMemoryUsage();
        long usedMemoryAfter = afterUsage.getUsed();
        long endCpuTime = osBean.getProcessCpuTime();
        long elapsedCpuTime = endCpuTime - startCpuTime;
        double elapsedTime = endTime - startTime;
        double cpuUsage = elapsedCpuTime / elapsedTime * 100;
        try (FileWriter log = new FileWriter("log.txt", true)) {
            log.write("Java:\n");
            log.write("Execution time: " + elapsedTime/1_000_000 + "ms\n");
            log.write("Memory usage change: " + (usedMemoryAfter - usedMemoryBefore) / 1024 + " KB\n");
            log.write(String.format("CPU usage: %.2f%%\n\n", cpuUsage));
        } catch (IOException e) {
            System.err.println("Error writing to log file: " + e.getMessage());
        }
    }
}
