import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 创建输出目录
os.makedirs('sum_analysis_charts', exist_ok=True)

# 读取CSV文件
df = pd.read_csv('/home/gump/pall/add/sum_algorithm_results6.csv')

# 设置更好的算法名称用于显示
algorithm_names = {
    '平凡算法(μs)': 'Naive Sum',
    '两路链式(μs)': 'Two-way Sum',
    '递归两两相加(μs)': 'Recursive Sum',
    '原地两两相加(μs)': 'In-place Sum',
    '展开4路(μs)': '4-way Unrolled Sum',
    '展开8路分块(μs)': '8-way Blocked Sum'
}

# 创建加速比列名到算法列名的映射
speedup_to_algo = {
    '两路加速比': '两路链式(μs)',
    '递归加速比': '递归两两相加(μs)',
    '两两相加加速比': '原地两两相加(μs)',
    '展开4路加速比': '展开4路(μs)',
    '展开8路加速比': '展开8路分块(μs)'
}

# 设置线型和标记样式
line_styles = ['-o', '-s', '-^', '-d', '-*', '-v']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# 设置缓存边界
bytes_per_double = 8
l1_size_bytes = (896 * 1024) / 24  # 约37KB
l1_size = int(l1_size_bytes / bytes_per_double)  # 约4600个double
l2_size_bytes = (32 * 1024 * 1024) / 12  # 约2.67MB
l2_size = int(l2_size_bytes / bytes_per_double)  # 约333000个double
l3_size_bytes = 36 * 1024 * 1024  # 36MB
l3_size = int(l3_size_bytes / bytes_per_double)  # 约4500000个double

# ========== 1. 执行时间随数据规模变化图 (对数坐标) ==========
plt.figure(figsize=(14, 8))

# 绘制各算法执行时间
for i, algo in enumerate([col for col in df.columns if 'μs' in col]):
    if '平凡算法' in algo:
        linewidth = 3  # 基准算法线更粗
        zorder = 10
    else:
        linewidth = 2
        zorder = i
    plt.loglog(df['数据大小'], df[algo], line_styles[i], 
              label=algorithm_names[algo], color=colors[i], 
              linewidth=linewidth, markersize=8, zorder=zorder)

# 添加缓存边界线
plt.axvline(x=l1_size, color='gray', linestyle='--', alpha=0.7, label='L1 Cache (~4.6K)')
plt.axvline(x=l2_size, color='gray', linestyle=':', alpha=0.7, label='L2 Cache (~333K)')
plt.axvline(x=l3_size, color='gray', linestyle='-.', alpha=0.7, label='L3 Cache (~4.5M)')

# 标记缓存区域
plt.fill_betweenx([plt.ylim()[0], plt.ylim()[1]*10], 0, l1_size, color='blue', alpha=0.05)
plt.fill_betweenx([plt.ylim()[0], plt.ylim()[1]*10], l1_size, l2_size, color='green', alpha=0.05)
plt.fill_betweenx([plt.ylim()[0], plt.ylim()[1]*10], l2_size, l3_size, color='yellow', alpha=0.05)
plt.fill_betweenx([plt.ylim()[0], plt.ylim()[1]*10], l3_size, df['数据大小'].max()*2, color='red', alpha=0.05)

# 添加缓存边界文本
plt.text(l1_size/3, plt.ylim()[1]/2, 'L1 Region', rotation=90, va='center', fontsize=12, 
         bbox=dict(boxstyle="round", fc="white", ec="blue", alpha=0.8, pad=0.3))
plt.text(l1_size*5, plt.ylim()[1]/2, 'L2 Region', rotation=90, va='center', fontsize=12, 
         bbox=dict(boxstyle="round", fc="white", ec="green", alpha=0.8, pad=0.3))
plt.text(l2_size*5, plt.ylim()[1]/2, 'L3 Region', rotation=90, va='center', fontsize=12, 
         bbox=dict(boxstyle="round", fc="white", ec="orange", alpha=0.8, pad=0.3))
plt.text(l3_size*5, plt.ylim()[1]/2, 'Memory Region', rotation=90, va='center', fontsize=12, 
         bbox=dict(boxstyle="round", fc="white", ec="red", alpha=0.8, pad=0.3))

plt.title('Array Summation: Execution Time vs Data Size (Log-Log Scale)', fontsize=16)
plt.xlabel('Array Size (Number of Doubles)', fontsize=14)
plt.ylabel('Execution Time (microseconds)', fontsize=14)
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.legend(loc='best', fontsize=12)
plt.tight_layout()
plt.savefig('sum_analysis_charts/execution_time_vs_size.png', dpi=300)
plt.close()

# ========== 2. 加速比随数据规模变化图 (半对数坐标) ==========
plt.figure(figsize=(14, 8))

# 绘制各算法加速比
speedup_cols = [col for col in df.columns if '加速比' in col]
for i, col in enumerate(speedup_cols):
    # 使用映射字典获取对应的算法名称
    algo_col = speedup_to_algo[col]
    plt.semilogx(df['数据大小'], df[col], line_styles[i+1], 
                label=algorithm_names[algo_col], color=colors[i+1],
                linewidth=2, markersize=8)

# 添加缓存边界线
plt.axvline(x=l1_size, color='gray', linestyle='--', alpha=0.7, label='L1 Cache (~4.6K)')
plt.axvline(x=l2_size, color='gray', linestyle=':', alpha=0.7, label='L2 Cache (~333K)')
plt.axvline(x=l3_size, color='gray', linestyle='-.', alpha=0.7, label='L3 Cache (~4.5M)')

# 添加基准线
plt.axhline(y=1.0, color='r', linestyle='-', alpha=0.5, label='No Speedup (1.0)')

# 标记缓存区域
plt.fill_betweenx([0, plt.ylim()[1]*1.2], 0, l1_size, color='blue', alpha=0.05)
plt.fill_betweenx([0, plt.ylim()[1]*1.2], l1_size, l2_size, color='green', alpha=0.05)
plt.fill_betweenx([0, plt.ylim()[1]*1.2], l2_size, l3_size, color='yellow', alpha=0.05)
plt.fill_betweenx([0, plt.ylim()[1]*1.2], l3_size, df['数据大小'].max()*2, color='red', alpha=0.05)

# 找出每个算法的最大加速比
for i, col in enumerate(speedup_cols):
    max_speedup = df[col].max()
    max_idx = df[col].idxmax()
    max_size = df.loc[max_idx, '数据大小']
    plt.plot([max_size], [max_speedup], 'k*', markersize=12)
    plt.annotate(f'Max: {max_speedup:.2f}x\n@{max_size}', 
                 xy=(max_size, max_speedup),
                 xytext=(max_size*1.5, max_speedup*0.95),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1),
                 fontsize=10, bbox=dict(boxstyle="round", fc="yellow", alpha=0.8))

plt.title('Array Summation: Speedup Ratio vs Data Size', fontsize=16)
plt.xlabel('Array Size (Number of Doubles)', fontsize=14)
plt.ylabel('Speedup Ratio (vs Naive)', fontsize=14)
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.legend(loc='best', fontsize=12)
plt.tight_layout()
plt.savefig('sum_analysis_charts/speedup_vs_size.png', dpi=300)
plt.close()

# ========== 3. 不同缓存区域的平均加速比 ==========
plt.figure(figsize=(14, 8))

# 定义缓存区域
regions = [
    (0, l1_size, 'L1 Region'),
    (l1_size, l2_size, 'L2 Region'),
    (l2_size, l3_size, 'L3 Region'),
    (l3_size, float('inf'), 'Memory Region')
]

# 为每个区域计算平均加速比
region_data = []
for start, end, name in regions:
    region_df = df[(df['数据大小'] >= start) & (df['数据大小'] < end)]
    if len(region_df) == 0:
        continue
    
    region_means = {}
    for col in speedup_cols:
        algo_col = speedup_to_algo[col]  # 使用映射字典
        region_means[algorithm_names[algo_col]] = region_df[col].mean()
    
    region_data.append((name, region_means))

# 绘制分组条形图
n_algorithms = len(speedup_cols)
bar_width = 0.15
index = np.arange(len(region_data))

for i, col in enumerate(speedup_cols):
    algo_col = speedup_to_algo[col]  # 使用映射字典
    display_name = algorithm_names[algo_col]
    
    means = [d[1].get(display_name, 0) for d in region_data]
    pos = index + (i - n_algorithms/2 + 0.5) * bar_width
    
    bars = plt.bar(pos, means, bar_width, label=display_name, color=colors[i+1])
    
    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.2f}', ha='center', va='bottom', rotation=0, fontsize=8)

plt.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='No Speedup (1.0)')
plt.title('Average Speedup by Cache Region', fontsize=16)
plt.xlabel('Cache Region', fontsize=14)
plt.ylabel('Average Speedup Ratio', fontsize=14)
plt.xticks(index, [d[0] for d in region_data])
plt.legend(loc='upper left', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('sum_analysis_charts/average_speedup_by_region.png', dpi=300)
plt.close()

# ========== 4. 最快算法随数据规模变化 ==========
plt.figure(figsize=(14, 8))

# 找出每个规模下执行时间最短的算法
fastest_algo_idx = []
fastest_time = []
data_sizes = []

for idx, row in df.iterrows():
    time_cols = [col for col in df.columns if 'μs' in col]
    times = [row[col] for col in time_cols]
    min_time_idx = np.argmin(times)
    min_time = times[min_time_idx]
    
    fastest_algo_idx.append(min_time_idx)
    fastest_time.append(min_time)
    data_sizes.append(row['数据大小'])

# 绘制数据点
plt.semilogx(data_sizes, fastest_algo_idx, 'ko-', markersize=8)

# 添加缓存边界线
plt.axvline(x=l1_size, color='gray', linestyle='--', alpha=0.7, label='L1 Cache (~4.6K)')
plt.axvline(x=l2_size, color='gray', linestyle=':', alpha=0.7, label='L2 Cache (~333K)')
plt.axvline(x=l3_size, color='gray', linestyle='-.', alpha=0.7, label='L3 Cache (~4.5M)')

# 设置y轴刻度为算法名称
time_cols = [col for col in df.columns if 'μs' in col]
alg_names = [algorithm_names[col] for col in time_cols]
plt.yticks(range(len(alg_names)), alg_names)

plt.title('Fastest Algorithm by Data Size', fontsize=16)
plt.xlabel('Array Size (Number of Doubles)', fontsize=14)
plt.ylabel('Algorithm', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend(loc='upper right', fontsize=12)
plt.tight_layout()
plt.savefig('sum_analysis_charts/fastest_algorithm_by_size.png', dpi=300)
plt.close()

# ========== 5. 算法性能可扩展性分析 ==========
plt.figure(figsize=(14, 8))

# 计算执行时间增长率
growth_data = {}
for i, algo in enumerate([col for col in df.columns if 'μs' in col]):
    # 选择几个不同规模的数据点计算增长率
    sizes = [1024, 65536, 4000000, 67108864]  # 1K, 64K, 4M, 64M
    
    # 查找最近的数据点
    times = []
    actual_sizes = []
    for size in sizes:
        closest_idx = (df['数据大小'] - size).abs().idxmin()
        times.append(df.loc[closest_idx, algo])
        actual_sizes.append(df.loc[closest_idx, '数据大小'])
    
    # 计算不同规模间的增长率
    growth_rates = []
    for j in range(1, len(times)):
        growth = times[j] / times[j-1]
        size_ratio = actual_sizes[j] / actual_sizes[j-1]
        normalized_growth = growth / size_ratio  # 归一化为"每翻倍数据量的增长"
        growth_rates.append(normalized_growth)
    
    growth_data[algorithm_names[algo]] = growth_rates

# 创建分组条形图
n_regions = len(growth_data[list(growth_data.keys())[0]])
bar_width = 0.12
index = np.arange(n_regions)
comparison_labels = ['1K→64K', '64K→4M', '4M→64M']

for i, (algo, rates) in enumerate(growth_data.items()):
    pos = index + (i - len(growth_data)/2 + 0.5) * bar_width
    bars = plt.bar(pos, rates, bar_width, label=algo, color=colors[i])
    
    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                 f'{height:.2f}', ha='center', va='bottom', rotation=0, fontsize=8)

# 添加理想增长线
plt.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='Linear Scaling (1.0)')

plt.title('Algorithm Scaling Efficiency (Lower is Better)', fontsize=16)
plt.xlabel('Size Comparison', fontsize=14)
plt.ylabel('Normalized Growth Rate', fontsize=14)
plt.xticks(index, comparison_labels)
plt.legend(loc='upper left', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('sum_analysis_charts/scaling_efficiency.png', dpi=300)
plt.close()

print("所有图表已生成在 sum_analysis_charts 目录中")