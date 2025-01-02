#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/resource.h>
#include <sys/times.h>
#include <unistd.h>

void bubbleSort(int arr[], int n) {
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

int main() {
    FILE *log_file = fopen("log.txt", "w");
    if (!log_file) {
        perror("Unable to open log file");
        return EXIT_FAILURE;
    }

    int arr[] = {2493, 3089, 4076, 2354, 4385, /*... (your array data) ...*/};
    int n = sizeof(arr)/sizeof(arr[0]);

    struct rusage usage_start, usage_end;
    clock_t start = clock();
    getrusage(RUSAGE_SELF, &usage_start);

    for (int i = 0; i < 1000; i++) {
        bubbleSort(arr, n);
    }

    clock_t end = clock();
    getrusage(RUSAGE_SELF, &usage_end);

    fprintf(log_file, "Execution time: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
    fprintf(log_file, "Memory usage (max RSS): %ld KB\n", usage_end.ru_maxrss - usage_start.ru_maxrss);
    fclose(log_file);
    return 0;
}
