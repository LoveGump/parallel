#include <iostream>
#include <random>
#include <functional>
#include <sys/time.h>
using namespace std;

// 获取当前时间（微秒级）
double get_time() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000000.0 + tv.tv_usec;
}

// 优化算法1：两路链式累加，减少指令依赖
double two_way_sum(const double* numbers, size_t size) {
    double sum1 = 0.0;
    double sum2 = 0.0;
    
    // 使用两个累加器交替累加
    size_t i = 0;
    for (; i + 1 < size; i += 2) {
        sum1 += numbers[i];
        sum2 += numbers[i + 1];
    }
    
    // 处理奇数长度的情况
    if (i < size) {
        sum1 += numbers[i];
    }
    
    return sum1 + sum2;
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
    const size_t size = 8192;
    const int runs = 1000; // 每个规模运行的次数
    
    random_device rd;// 随机数种子
    mt19937 gen(rd());// 随机数生成器
    uniform_real_distribution<> dis(-100.0, 100.0);// 生成-100到100之间的随机数
    
    // 生成随机数据
    double* data = new double[size];
        
    for (size_t i = 0; i < size; ++i) {
        data[i] = dis(gen);
    }
        
    // 测量算法执行时间
    double time_two_way = time_execution([&]() { 
        double result = two_way_sum(data, size); 
        // 使用volatile防止编译器优化掉计算
        volatile double prevent_optimize = result;
    }, runs);
        
    cout << runs << " " << size << " " << time_two_way << endl;
    
    // 释放内存
    delete[] data;
    
    return 0;
}