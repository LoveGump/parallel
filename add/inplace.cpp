#include <iostream>
#include <random>
#include <functional>
#include <sys/time.h>
#include <cstring>
using namespace std;

// 获取当前时间（微秒级）
double get_time() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000000.0 + tv.tv_usec;
}

// 优化算法3：原地两两相加
double in_place_pairwise_sum(double* data, size_t size) {
    if (size == 0) {
        return 0.0;
    }
    
    size_t n = size;
    size_t j = 0;
    size_t i = 0;
    
    while (n > 1) {
        j = 0;
        for (i = 0; i + 1 < n; i += 2, ++j) {
            data[j] = data[i] + data[i + 1];
        }
        if (n % 2 == 1) {
            data[j++] = data[n - 1]; // 处理奇数
        }
        n = j;
    }
    
    return n == 0 ? 0.0 : data[0];
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
    const int runs = 1000; // 每个规模运行的次数
    
    random_device rd;// 随机数种子
    mt19937 gen(rd());// 随机数生成器
    uniform_real_distribution<> dis(-100.0, 100.0);// 生成-100到100之间的随机数
    
    // 生成随机数据
    double* data = new double[size];
    double* data_copy = new double[size]; // 用于原地算法的副本
        
    for (size_t i = 0; i < size; ++i) {
        data[i] = dis(gen);
    }
        
    // 测量算法执行时间
    double time_in_place = time_execution([&]() {
        // 复制数据，因为原地算法会修改数据
        memcpy(data_copy, data, size * sizeof(double));
        double result = in_place_pairwise_sum(data_copy, size);
        // 使用volatile防止编译器优化掉计算
        volatile double prevent_optimize = result;
    }, runs);
        
    cout << runs << " " << size << " " << time_in_place << endl;
    
    // 释放内存
    delete[] data;
    delete[] data_copy;
    
    return 0;
}