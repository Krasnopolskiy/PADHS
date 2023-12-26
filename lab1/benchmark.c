#include <stdio.h>
#include <time.h>

void benchmark() {
    long long count = 0;
    for (long long i = 0; i < 20000000000; i++) { count++; }
}

int main() {
    clock_t start, end;
    double cpu_time_used;

    start = clock();
    benchmark();
    end = clock();

    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    printf("The task took %f seconds to execute.\n", cpu_time_used);

    return 0;
}
