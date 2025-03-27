#include <iostream>
#include <random>
#include <iomanip>
#include <functional>
#include <sys/time.h>
using namespace std;
// 获取当前时间（微秒级）
double get_time() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000000.0 + tv.tv_usec;
}

// 朴素算法（链式）：逐个累加
double naive_sum(const double* numbers, size_t size) {
    double sum = 0.0;
    for (size_t i = 0; i < size; ++i) {
        sum += numbers[i];
    }
    return sum;
}

// 测量函数执行时间
template<typename Func>
double time_execution(Func&& func, int runs) {
    double* times = new double[runs];
    
    for (int i = 0; i < runs; ++i) {
        double start = get_time();
        func();
        double end = get_time();
        
        times[i] = end - start;
    }
    
    // 计算平均时间
    double total = 0.0;
    for (int i = 0; i < runs; ++i) {
        total += times[i];
    }
    
    delete[] times;
    return total / runs;
}

int main() {
    
    const size_t size= 4096;
    const int runs = 1000; // 每个规模运行的次数
    
    random_device rd;// 随机数种子
    mt19937 gen(rd());// 随机数生成器
    uniform_real_distribution<> dis(-100.0, 100.0);// 生成-100到100之间的随机数
    

    
    // 生成随机数据
    double* data = new double[size];
        
    for (size_t i = 0; i < size; ++i) {
        data[i] = dis(gen);
    }
        
        // 测量朴素算法执行时间
    double time_naive = time_execution([&]() { 
        double result = naive_sum(data, size); 
        // 使用volatile防止编译器优化掉计算
        volatile double prevent_optimize = result;
    }, runs);
        
    cout <<runs<<" "<<  size << " " << time_naive << endl;
        // 释放内存
    delete[] data;
    
    return 0;
}