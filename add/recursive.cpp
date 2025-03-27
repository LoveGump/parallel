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

// 优化算法2：递归两两相加
double recursive_sum_helper(const double* numbers, size_t start, size_t end) {
    if (start > end) {
        return 0.0;
    }
    if (start == end) {
        return numbers[start];
    }
    if (start + 1 == end) {
        return numbers[start] + numbers[end];
    }
    
    size_t mid = start + (end - start) / 2;
    return recursive_sum_helper(numbers, start, mid) + 
           recursive_sum_helper(numbers, mid + 1, end);
}

// 递归算法的包装函数
double recursive_sum(const double* numbers, size_t size) {
    if (size == 0) {
        return 0.0;
    }
    return recursive_sum_helper(numbers, 0, size - 1);
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
    double time_recursive = time_execution([&]() { 
        double result = recursive_sum(data, size); 
        // 使用volatile防止编译器优化掉计算
        volatile double prevent_optimize = result;
    }, runs);
        
    cout << runs << " " << size << " " << time_recursive << endl;
    
    // 释放内存
    delete[] data;
    
    return 0;
}