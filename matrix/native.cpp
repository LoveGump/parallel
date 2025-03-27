#include <iostream>
#include <cstdlib>
#include <sys/time.h>
#include <cstring>
#include <random>
#include <iomanip>
#include <algorithm>

using namespace std;
constexpr int MAXN = 10000;

double A[MAXN][MAXN];
double v[MAXN];
double result_naive[MAXN], result_opt[MAXN];

void fill_random(int n) {
    // 使用C++随机数生成器
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<double> dist(0.0, 1.0);
    
    for (int i = 0; i < n; ++i) {
        v[i] = dist(gen);
        for (int j = 0; j < n; ++j) {
            A[i][j] = dist(gen);
        }
    }
}

void naive_column_dot(int n, double A[][MAXN], double v[], double result[]) {
    memset(result, 0, n * sizeof(double));
    
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            result[j] += A[i][j] * v[i];
        }
    }
}

int main(int argc, char *argv[]) {
    int n = 1024;
    int repeat = 100;

    cout << "重复: " << repeat << " 规模: " << n << endl;
    fill_random(n);

    // 保留gettimeofday计时
    struct timeval start, end;
    double elapsed;// 记录每次运行的时间

    // 计时naive算法
    double naive_total = 0.0;
    
    for (int r = 0; r < repeat; ++r) {
        gettimeofday(&start, nullptr);
        naive_column_dot(n, A, v, result_naive);
        gettimeofday(&end, nullptr);
        
        elapsed = (end.tv_sec - start.tv_sec) * 1e6;
        elapsed = (elapsed + (end.tv_usec - start.tv_usec)); // 微秒单位
        
        naive_total += elapsed;
    }
    
    double naive_avg = naive_total / repeat;
    
    // 打印统计信息
    cout << fixed << setprecision(2);
    cout << "平均时间: " << naive_avg << " us" << endl;

    return 0;
}