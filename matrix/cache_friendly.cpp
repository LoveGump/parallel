#include <iostream>
#include <cstdlib>
#include <sys/time.h>
#include <cstring>
#include <random>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <fstream>

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
    int repeat = 10;
    
    // 修正命令行参数处理
    if(argc > 1) {
        n = stoi(argv[1]);
    }
    
    cout << "重复" << repeat << " 规模" << n <<endl;
    fill_random(n);

    // 保留gettimeofday计时
    struct timeval start, end;
    double elapsed;

    // 记录每次运行的时间
    vector<double> naive_times;
    vector<double> opt_times;

    // 计时naive算法
    double naive_total = 0.0;
    
    for (int r = 0; r < repeat; ++r) {
        gettimeofday(&start, nullptr);
        naive_column_dot(n, A, v, result_naive);
        gettimeofday(&end, nullptr);
        
        elapsed = (end.tv_sec - start.tv_sec) * 1e6;
        elapsed = (elapsed + (end.tv_usec - start.tv_usec)); // 不再除以1e6，保持微秒单位
        
        naive_times.push_back(elapsed);
        naive_total += elapsed;
    }
    
    double naive_avg = naive_total / repeat;
    
    // 计时优化算法
    double opt_total = 0.0;
    
    for (int r = 0; r < repeat; ++r) {
        gettimeofday(&start, nullptr);
        cache_friendly_column_dot(n, A, v, result_opt);
        gettimeofday(&end, nullptr);
        
        elapsed = (end.tv_sec - start.tv_sec) * 1e6;
        elapsed = (elapsed + (end.tv_usec - start.tv_usec)); // 不再除以1e6，保持微秒单位
        
        opt_times.push_back(elapsed);
        opt_total += elapsed;
    }
    
    double opt_avg = opt_total / repeat;
    double speedup = naive_avg / opt_avg;

    // 打印统计信息
    cout << fixed << setprecision(2); // 减少小数位数，因为微秒单位足够小
    cout << "\n=== Naive 算法统计 ===" << endl;
    cout << "平均时间: " << naive_avg << " us" << endl;
    
    cout << "\n=== 优化算法统计 ===" << endl;
    cout << "平均时间: " << opt_avg << " us" << endl;
    
    cout << "\n=== 性能比较 ===" << endl;
    cout << "加速比(Naive/Optimized): " << speedup << "x" << endl;

    // 将结果保存到CSV文件
    const string csv_filename = "matrix_performance_results.csv";
    
    // 检查文件是否存在
    bool file_exists = false;
    ifstream check_file(csv_filename);
    if (check_file.good()) {
        file_exists = true;
    }
    check_file.close();
    
    // 以追加模式打开文件
    ofstream csv_file;
    csv_file.open(csv_filename, ios::app);
    
    // 如果文件不存在，写入表头
    if (!file_exists) {
        csv_file << "规模,朴素算法(us),优化算法(us),加速比" << endl;
    }
    
    // 写入当前测试结果
    csv_file << n << "," << fixed << setprecision(2) << naive_avg << "," 
             << opt_avg << "," << speedup << endl;
    
    csv_file.close();
    
    cout << "\n结果已添加到文件: " << csv_filename << endl;

    return 0;
}