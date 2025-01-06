import time
import os

def read_cpu_stats():
    with open("/proc/stat", "r") as file:
        first_line = file.readline()
        if first_line.startswith("cpu "):
            return list(map(int, first_line.split()[1:]))
        else:
            raise ValueError("Unexpected format in /proc/stat")

def calculate_total(stats):
    return sum(stats)

if __name__ == "__main__":
    arr = list(range(1, 1_000_001))
    
    # Initial CPU stats
    cpu_stats_before = read_cpu_stats()
    total_before = calculate_total(cpu_stats_before)
    idle_before = cpu_stats_before[3]
    
    # Measure execution time
    start_time_ns = time.perf_counter_ns()
    arr = sorted(arr, reverse=True)
    end_time_ns = time.perf_counter_ns()
    execution_time = (end_time_ns - start_time_ns) / 1_000_000  # Convert to milliseconds

    # Final CPU stats
    cpu_stats_after = read_cpu_stats()
    total_after = calculate_total(cpu_stats_after)
    idle_after = cpu_stats_after[3]

    # Calculate CPU usage percentage
    idle_diff = idle_after - idle_before
    total_diff = total_after - total_before
    cpu_usage = 100.0 * (1.0 - (idle_diff / total_diff))

    # Memory usage (Linux-specific)
    with open("/proc/self/statm", "r") as file:
        resident_pages = int(file.readline().split()[1])
        memory_usage = resident_pages * 4096  # Convert pages to bytes

    # Log results
    with open("log.txt", "a") as log:
        log.write("Python:\n")
        log.write(f"Execution time: {execution_time:.9f}ms\n")
        log.write(f"Memory usage: {memory_usage / 1024:.2f} KB\n")
        log.write(f"CPU usage: {cpu_usage:.2f}%\n\n")
