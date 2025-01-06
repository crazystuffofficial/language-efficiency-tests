#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/resource.h>
#include <unistd.h>
#include <string.h>

long get_cpu_time() {
    FILE* file = fopen("/proc/stat", "r");
    if (!file) {
        perror("Failed to open /proc/stat");
        return -1;
    }
    char buffer[256];
    if (fgets(buffer, sizeof(buffer), file) == NULL) {
        perror("Failed to read /proc/stat");
        fclose(file);
        return -1;
    }
    fclose(file);
    long user, nice, system;
    if (sscanf(buffer, "cpu %ld %ld %ld", &user, &nice, &system) != 3) {
        perror("Failed to parse /proc/stat");
        return -1;
    }
    return user + nice + system;
}

int compare(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

long get_time_in_ns() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1e9 + ts.tv_nsec;
}

int main() {
    int size = 1000000;
    int* arr = malloc(size * sizeof(int));
    if (!arr) {
        perror("Memory allocation failed");
        return 1;
    }

    for (int i = 0; i < size; i++) {
        arr[i] = size - i;
    }

    long cpu_start = get_cpu_time();
    if (cpu_start == -1) {
        free(arr);
        return 1;
    }

    long start_time = get_time_in_ns();

    qsort(arr, size, sizeof(int), compare);

    long end_time = get_time_in_ns();
    long cpu_end = get_cpu_time();
    if (cpu_end == -1) {
        free(arr);
        return 1;
    }

    // Calculate elapsed time in seconds
    double elapsed_time = (end_time - start_time) / 1e9;

    // Calculate the change in CPU usage as a percentage
    long cpu_diff = cpu_end - cpu_start;
    double cpu_percentage = ((double)cpu_diff / sysconf(_SC_CLK_TCK)) / 
                            (elapsed_time * sysconf(_SC_NPROCESSORS_ONLN)) * 100;

    FILE* log = fopen("log.txt", "a");
    if (!log) {
        perror("Failed to open log file");
        free(arr);
        return 1;
    }

    fprintf(log, "C:\n");
    fprintf(log, "Elapsed time: %.9f seconds\n", elapsed_time);
    fprintf(log, "CPU usage change: %.2f%%\n", cpu_percentage);
    fclose(log);

    free(arr);
    return 0;
}
