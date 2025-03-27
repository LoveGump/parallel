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

// 新增: 优化版循环展开加法（8路展开+缓存分块+编译器向量化提示）
double unrolled_sum(const double* numbers, size_t size) {
    // 如果数组太小，使用简单方法避免额外开销
    if (size <= 16) {
        double sum = 0.0;
        for (size_t i = 0; i < size; ++i) {
            sum += numbers[i];
        }
        return sum;
    }
    
    // 缓存友好的分块大小（约64KB，适应L1缓存）
    const size_t BLOCK_SIZE = 8192;
    const size_t num_blocks = (size + BLOCK_SIZE - 1) / BLOCK_SIZE;
    
    double total_sum = 0.0;
    
    // 按块处理数据，提高缓存局部性
    for (size_t block = 0; block < num_blocks; ++block) {
        const size_t block_start = block * BLOCK_SIZE;
        const size_t block_end = std::min(block_start + BLOCK_SIZE, size);
        
        // 8路循环展开
        double sum0 = 0.0, sum1 = 0.0, sum2 = 0.0, sum3 = 0.0;
        double sum4 = 0.0, sum5 = 0.0, sum6 = 0.0, sum7 = 0.0;
        
        // 使用索引代替指针算术，更容易被向量化
        size_t i = block_start;
        
        // 主要8路循环
        #pragma GCC ivdep // 告诉编译器可以忽略潜在的依赖关系
        for (; i + 7 < block_end; i += 8) {
            sum0 += numbers[i];
            sum1 += numbers[i+1];
            sum2 += numbers[i+2];
            sum3 += numbers[i+3];
            sum4 += numbers[i+4];
            sum5 += numbers[i+5];
            sum6 += numbers[i+6];
            sum7 += numbers[i+7];
        }
        
        // 处理剩余元素
        for (; i < block_end; ++i) {
            sum0 += numbers[i];
        }
        
        // 合并部分和
        total_sum += (sum0 + sum1) + (sum2 + sum3) + (sum4 + sum5) + (sum6 + sum7);
    }
    
    return total_sum;
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