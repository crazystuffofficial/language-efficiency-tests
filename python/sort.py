import time
import psutil
import os
if __name__ == "__main__":
    arr = list(range(1, 1_000_001))
    process = psutil.Process(os.getpid())
    start_cpu_percent = psutil.cpu_percent(interval=None)
    start_time_ns = time.perf_counter_ns()
    start_memory = process.memory_info().rss
    arr = sorted(arr, reverse=True)
    end_time_ns = time.perf_counter_ns()
    end_memory = process.memory_info().rss
    end_cpu_percent = psutil.cpu_percent(interval=None)
    execution_time = (end_time_ns - start_time_ns) / 1_000_000
    with open("log.txt", "a") as log:
        log.write("Python: \n")
        log.write(f"Execution time: {execution_time:.9f}ms\n")
        log.write(f"Memory usage change: {(end_memory - start_memory) / 1024:.2f} KB\n")
        log.write(f"CPU usage: {end_cpu_percent:.2f}%\n\n")
