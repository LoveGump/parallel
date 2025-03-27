#include <iostream>
#include <random>
#include <iomanip>
#include <functional>
#include <sys/time.h>
using namespace std;

// 获取当前时间（微秒级）
double get_time() {
    struct timeval tv;
    gettimeofday(&tv, nullptr);
    return tv.tv_sec * 1000000.0 + tv.tv_usec;
}

// 循环展开优化版本（展开4次）
double unrolled_sum(const double* numbers, size_t size) {
    double sum0 = 0.0, sum1 = 0.0, sum2 = 0.0, sum3 = 0.0;
    const double* ptr = numbers;
    const double* end = ptr + size;

    // 主循环：每次处理4个元素
    for (; ptr + 3 < end; ptr += 4) {
        sum0 += ptr[0];
        sum1 += ptr[1];
        sum2 += ptr[2];
        sum3 += ptr[3];
    }

    // 合并部分和
    double sum = sum0 + sum1 + sum2 + sum3;

    // 处理余数元素
    for (; ptr < end; ++ptr) {
        sum += *ptr;
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
    const size_t size = 4096;
    const int runs = 1000;
    
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(-100.0, 100.0);
    
    // 生成随机数据
    double* data = new double[size];
    for (size_t i = 0; i < size; ++i) {
        data[i] = dis(gen);
    }
    

    
    // 测量循环展开算法
    double time_unrolled = time_execution([&]() { 
        volatile double result = unrolled_sum(data, size);
    }, runs);
    
    // 输出结果
    cout << "Size: " << size 
         << " | Runs: " << runs 
        
         << "\nUnrolled Time (µs): " << time_unrolled ;
         
    
    delete[] data;
    return 0;
}