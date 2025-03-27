#include <iostream>
#include <random>
#include <iomanip>
#include <functional>
#include <sys/time.h>
#include <cmath>
#include <cstring>
#include <fstream>  // 添加文件流头文件

// 获取当前时间（微秒级）
double get_time() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000000.0 + tv.tv_usec;
}

// 平凡算法（链式）：逐个累加
double naive_sum(const double* numbers, size_t size) {
    double sum = 0.0;
    for (size_t i = 0; i < size; ++i) {
        sum += numbers[i];
    }
    return sum;
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
    const size_t data_sizes[] = {
        // L1d缓存边界附近 (单核~37KB, 约4600个double)
        1024,             // 2^10 = 1,024   (8KB)
        2048,             // 2^11 = 2,048   (16KB)
        3000,             // ~24KB
        4000,             // ~32KB
        4600,             // ~37KB - L1d大小
        5000,             // ~40KB
        6000,             // ~48KB
        8192,             // 2^13 = 8,192   (64KB)
        
        // L2缓存边界附近 (每L2约2.67MB, 约333K个double)
        65536,            // 2^16 = 65,536  (512KB)
        131072,           // 2^17 = 131,072 (1MB)
        200000,           // ~1.6MB
        262144,           // 2^18 = 262,144 (2MB)
        330000,           // ~2.6MB - L2大小
        350000,           // ~2.8MB
        400000,           // ~3.2MB
        524288,           // 2^19 = 524,288 (4MB)
        
        // L3缓存边界附近 (36MB, 约4.5M个double)
        1048576,          // 2^20 = 1,048,576 (8MB)
        2097152,          // 2^21 = 2,097,152 (16MB)
        3000000,          // ~24MB
        4000000,          // ~32MB
        4500000,          // ~36MB - L3大小
        5000000,          // ~40MB
        6000000,          // ~48MB
        8388608,          // 2^23 = 8,388,608 (64MB)
        
        // 大规模数据测试
        16777216,         // 2^24 = 16,777,216 (128MB)
        33554432,         // 2^25 = 33,554,432 (256MB)
        67108864,         // 2^26 = 67,108,864 (512MB)
    };
    const int runs = 3; // 每个算法运行的次数
    
    // 创建CSV文件
    std::ofstream csv_file("sum_algorithm_results.csv");
    if (!csv_file.is_open()) {
        std::cerr << "无法创建CSV文件！" << std::endl;
        return 1;
    }
    
    // 写入CSV表头
    csv_file << "数据大小,平凡算法(μs),两路链式(μs),递归两两相加(μs),原地两两相加(μs),两路加速比,递归加速比,两两相加加速比\n";
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(-100.0, 100.0);
    
    std::cout << "计算N个数之和的算法性能比较：\n\n";
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "| 数据大小 | 平凡算法 (μs) | 两路链式 (μs) | 递归两两相加 (μs) | 原地两两相加(μs) | 两路加速比 | 递归加速比 | 两两相加加速比 |\n";
    std::cout << "|----------|--------------|--------------|-----------------|-----------------|------------|------------|---------------|\n";
    
    for (auto size : data_sizes) {
        // 生成随机数据
        double* data = new double[size];
        double* data_copy = new double[size]; // 用于原地算法的副本
        
        for (size_t i = 0; i < size; ++i) {
            data[i] = dis(gen);
        }
        
        // 验证结果的正确性
        double reference_result = naive_sum(data, size);
        double two_way_result = two_way_sum(data, size);
        double recursive_result = recursive_sum(data, size);
        
        // 为原地算法复制一份数据
        std::memcpy(data_copy, data, size * sizeof(double));
        double in_place_result = in_place_pairwise_sum(data_copy, size);

        // 确保所有算法返回相同的结果（考虑到浮点误差）
        const double epsilon = 1e-2;
        bool results_match = 
            std::abs(reference_result - two_way_result) < epsilon &&
            std::abs(reference_result - recursive_result) < epsilon &&
            std::abs(reference_result - in_place_result) < epsilon;

        if (!results_match) {
            std::cout << "警告：算法结果不一致！\n";
            std::cout << "平凡算法: " << reference_result << "\n";
            std::cout << "两路链式: " << two_way_result << "\n";
            std::cout << "递归算法: " << recursive_result << "\n";
            std::cout << "原地两两相加: " << in_place_result << "\n";
        }
        
        // 测量各算法的执行时间
        double time_naive = time_execution([&]() { naive_sum(data, size); }, runs);
        double time_two_way = time_execution([&]() { two_way_sum(data, size); }, runs);
        double time_recursive = time_execution([&]() { recursive_sum(data, size); }, runs);
        
        // 原地算法每次需要复制一份新数据
        double time_in_place = time_execution([&]() {
            std::memcpy(data_copy, data, size * sizeof(double));
            in_place_pairwise_sum(data_copy, size);
        }, runs);
        
        // 计算加速比
        double speedup_two_way = time_naive / time_two_way;
        double speedup_recursive = time_naive / time_recursive;
        double speedup_in_place = time_naive / time_in_place;
        
        // 输出结果到控制台
        std::cout << "| " << std::setw(8) << size << " | " 
                  << std::setw(12) << time_naive << " | " 
                  << std::setw(12) << time_two_way << " | " 
                  << std::setw(15) << time_recursive << " | " 
                  << std::setw(15) << time_in_place << " | " 
                  << std::setw(10) << speedup_two_way << " | " 
                  << std::setw(10) << speedup_recursive << " | " 
                  << std::setw(13) << speedup_in_place << " |\n";
        
        // 写入结果到CSV文件
        csv_file << size << ","
                 << time_naive << ","
                 << time_two_way << ","
                 << time_recursive << ","
                 << time_in_place << ","
                 << speedup_two_way << ","
                 << speedup_recursive << ","
                 << speedup_in_place << "\n";
        
        // 释放内存
        delete[] data;
        delete[] data_copy;
    }
    
    // 关闭CSV文件
    csv_file.close();
    std::cout << "\n结果已保存到 sum_algorithm_results.csv" << std::endl;
    
    return 0;
}