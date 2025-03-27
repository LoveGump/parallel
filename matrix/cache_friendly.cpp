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


void cache_friendly_column_dot(int n, double A[][MAXN], double v[], double result[]) {
    memset(result, 0, n * sizeof(double));

    for (int i = 0; i < n; ++i) {
        const double vi = v[i];
        for (int j = 0; j < n; ++j) {
            result[j] += A[i][j] * vi;
        }
    }
}

int main(int argc, char *argv[]) {
    int n = 1024;
    int repeat = 100;
    
    cout << "重复" << repeat << " 规模" << n <<endl;
    fill_random(n);

    // 保留gettimeofday计时
    struct timeval start, end;
    double elapsed;


    
    // 计时优化算法
    double opt_total = 0.0;
    
    for (int r = 0; r < repeat; ++r) {
        gettimeofday(&start, nullptr);
        cache_friendly_column_dot(n, A, v, result_opt);
        gettimeofday(&end, nullptr);
        
        elapsed = (end.tv_sec - start.tv_sec) * 1e6;
        elapsed = (elapsed + (end.tv_usec - start.tv_usec)); // 不再除以1e6，保持微秒单位
        
        opt_total += elapsed;
    }
    
    double opt_avg = opt_total / repeat;
    

    // 打印统计信息
    cout << fixed << setprecision(2); // 减少小数位数，因为微秒单位足够小
    cout << "平均时间: " << opt_avg << " us" << endl;

    return 0;
}