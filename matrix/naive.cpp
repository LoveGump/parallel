#include <iostream>
#include <cstdlib>
#include <sys/time.h>
#include <cstring>
#include <random>
#include <iomanip>

constexpr int MAXN = 10000;

double A[MAXN][MAXN];
double v[MAXN];
double result_naive[MAXN], result_opt[MAXN];

void fill_random(int n) {
    // 使用C++随机数生成器
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    
    for (int i = 0; i < n; ++i) {
        v[i] = dist(gen);
        for (int j = 0; j < n; ++j) {
            A[i][j] = dist(gen);
        }
    }
}
// 朴素算法 
void naive_column_dot(int n, double A[][MAXN], double v[], double result[]) {
    std::memset(result, 0, n * sizeof(double));
    
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            result[j] += A[i][j] * v[i];
        }
    }
}
int main(int argc, char *argv[]) {
    int n = 1024;
    int repeat = 100;
    
    // 修正命令行参数处理
    if(argc > 1) {
        n = std::stoi(argv[1]);
    }
    
    std::cout << "运行 " << repeat << " 次重复" << std::endl;
    fill_random(n);

    // 保留gettimeofday计时
    struct timeval start, end;
    double elapsed;

    // 计时naive算法
    gettimeofday(&start, nullptr);
    for (int r = 0; r < repeat; ++r) {
        naive_column_dot(n, A, v, result_naive);
    }

    
    gettimeofday(&end, nullptr);
    elapsed = (end.tv_sec - start.tv_sec) * 1e6;
    elapsed = (elapsed + (end.tv_usec - start.tv_usec)) / 1e6;
    std::cout << "Naive algorithm: " << std::fixed << std::setprecision(6) 
              << elapsed / repeat << " seconds" << std::endl;


    return 0;
}