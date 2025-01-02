import time
import psutil
import os

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

if __name__ == "__main__":
    arr = [2493, 3089, 4076, 2354, 4385, /*... (your array data) ...*/]
    process = psutil.Process(os.getpid())

    start_time = time.time()
    start_memory = process.memory_info().rss
    start_cpu = process.cpu_percent(interval=None)

    for _ in range(1000):
        bubble_sort(arr)

    end_time = time.time()
    end_memory = process.memory_info().rss
    end_cpu = process.cpu_percent(interval=None)

    with open("log.txt", "w") as log:
        log.write(f"Execution time: {end_time - start_time} seconds\n")
        log.write(f"Memory usage change: {(end_memory - start_memory) / 1024} KB\n")
        log.write(f"CPU usage change: {end_cpu - start_cpu} %\n")
