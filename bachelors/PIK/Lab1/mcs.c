#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <math.h>

#define NUM_SAMPLES 500000000

double func(double x) {
    return x*x*x;
}

int main(int argc, char *argv[]) {
    
    uint seed = (uint)time(NULL);
    long double totalSum = 0.0;
    long double totalSquaredDiff = 0.0;
    long double numSamples = NUM_SAMPLES;

    if (argc > 1){
        numSamples = atol(argv[1]);
        if (numSamples <= 0){
            fprintf(stderr,"Nije dobro ponovo unesite");
            return 1;
        }
        else{
            printf("Number of points: %Lf\n", numSamples);
        }
    }
    else{
        printf("Number of points not specified, default number of points is used: %d\n", NUM_SAMPLES);
    }
    clock_t start = clock();

    for (int i = 0; i < numSamples; ++i){
        long double x = (double)rand_r(&seed) / RAND_MAX;
        long double y = func(x * 10);
        totalSum += y;
        totalSquaredDiff += y * y;
    }

    clock_t end = clock();
    long double cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    long double result = (totalSum / numSamples) * 10;
    long double mean = totalSum / numSamples;
    long double squaredMean = totalSquaredDiff / numSamples;
    long double variance = squaredMean - mean * mean;
    long double error = sqrt(variance / numSamples);

    printf("dobiveni integral: %Lf\n", result);
    printf("Error (Standard Error): %Lf\n", error);
    printf("Elapsed time: %Lf\n", cpu_time_used);

    return 0;
}















