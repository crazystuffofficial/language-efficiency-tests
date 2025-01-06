import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;

public class sort {
    public static void main(String[] args) throws IOException {
        int size = 1_000_000;
        Integer[] arr = new Integer[size];
        for (int i = 0; i < size; i++) {
            arr[i] = i + 1;
        }

        // Memory usage before
        long usedMemoryBefore = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        // CPU usage before
        long[] cpuStatsBefore = getCpuStats();

        // Task execution
        long startTime = System.nanoTime();
        Arrays.sort(arr, Collections.reverseOrder());
        long endTime = System.nanoTime();

        // Memory usage after
        long usedMemoryAfter = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        // CPU usage after
        long[] cpuStatsAfter = getCpuStats();

        // Calculate CPU usage percentage
        long idleDiff = cpuStatsAfter[3] - cpuStatsBefore[3];
        long totalDiff = calculateTotal(cpuStatsAfter) - calculateTotal(cpuStatsBefore);
        double cpuUsage = 100.0 * (1.0 - ((double) idleDiff / totalDiff));

        // Execution time
        double elapsedTime = (endTime - startTime) / 1_000_000.0;

        // Log results
        try (FileWriter log = new FileWriter("log.txt", true)) {
            log.write("Java:\n");
            log.write("Execution time: " + elapsedTime + "ms\n");
            log.write("Memory usage change: " + (usedMemoryAfter - usedMemoryBefore) / 1024 + " KB\n");
            log.write(String.format("CPU usage: %.2f%%\n\n", cpuUsage));
        } catch (IOException e) {
            System.err.println("Error writing to log file: " + e.getMessage());
        }
    }

    private static long[] getCpuStats() throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader("/proc/stat"))) {
            String line = reader.readLine();
            if (line.startsWith("cpu ")) {
                String[] tokens = line.split("\\s+");
                long[] stats = new long[tokens.length - 1];
                for (int i = 1; i < tokens.length; i++) {
                    stats[i - 1] = Long.parseLong(tokens[i]);
                }
                return stats;
            } else {
                throw new IOException("Unexpected format in /proc/stat");
            }
        }
    }

    private static long calculateTotal(long[] stats) {
        long total = 0;
        for (long stat : stats) {
            total += stat;
        }
        return total;
    }
}
