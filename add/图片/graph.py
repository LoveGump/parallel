import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取CSV文件
df = pd.read_csv('/home/gump/pall/add/sum_algorithm_results.csv')

# 重命名列为英文
df = df.rename(columns={
    '数据大小': 'Data Size',
    '平凡算法(μs)': 'Naive Sum (μs)',
    '两路链式(μs)': 'Two-way Sum (μs)',
    '递归两两相加(μs)': 'Recursive Sum (μs)',
    '原地两两相加(μs)': 'In-place Sum (μs)',
    '两路加速比': 'Two-way Speedup',
    '递归加速比': 'Recursive Speedup',
    '两两相加加速比': 'In-place Speedup'
})

# 设置全局字体和样式
plt.rcParams['font.size'] = 12
plt.style.use('seaborn-v0_8-whitegrid')

# 设置缓存边界
# 基于实际系统信息设置精确的缓存边界
# 每个double占用8字节
bytes_per_double = 8

# L1d: 896 KiB 分布在24个实例上 (每实例约37.33 KiB)
l1_size_bytes = (896 * 1024) / 24  # 每核心L1d大小(字节)
l1_size = int(l1_size_bytes / bytes_per_double)  # 可容纳的double数量 ≈ 4667个double

# L2: 32 MiB 分布在12个实例上 (每实例约2.67 MiB)
l2_size_bytes = (32 * 1024 * 1024) / 12  # 每L2单元大小(字节)
l2_size = int(l2_size_bytes / bytes_per_double)  # 可容纳的double数量 ≈ 333,333个double

# L3: 36 MiB (全部核心共享)
l3_size_bytes = 36 * 1024 * 1024  # L3总大小(字节)
l3_size = int(l3_size_bytes / bytes_per_double)  # 可容纳的double数量 ≈ 4,500,000个double

# 输出精确的缓存大小信息
print(f"Cache size boundaries (in number of doubles):")
print(f"L1d: {l1_size} doubles ({l1_size_bytes/1024:.2f} KiB per core)")
print(f"L2: {l2_size} doubles ({l2_size_bytes/(1024*1024):.2f} MiB per unit)")
print(f"L3: {l3_size} doubles ({l3_size_bytes/(1024*1024):.2f} MiB shared)")

# 1. 执行时间比较图 (对数尺度)
plt.figure(figsize=(12, 8))
plt.loglog(df['Data Size'], df['Naive Sum (μs)'], 'ro-', label='Naive Sum', linewidth=2)
plt.loglog(df['Data Size'], df['Two-way Sum (μs)'], 'go-', label='Two-way Sum', linewidth=2)
plt.loglog(df['Data Size'], df['Recursive Sum (μs)'], 'bo-', label='Recursive Sum', linewidth=2)
plt.loglog(df['Data Size'], df['In-place Sum (μs)'], 'mo-', label='In-place Sum', linewidth=2)

# 添加缓存边界线
plt.axvline(x=l1_size, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=l2_size, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=l3_size, color='gray', linestyle='--', alpha=0.7)

# 标记缓存边界
plt.text(l1_size*1.1, plt.ylim()[0]*1.5, 'L1 Cache (37KB)', rotation=90, alpha=0.7)
plt.text(l2_size*1.1, plt.ylim()[0]*1.5, 'L2 Cache (2.67MB)', rotation=90, alpha=0.7)
plt.text(l3_size*1.1, plt.ylim()[0]*1.5, 'L3 Cache (36MB)', rotation=90, alpha=0.7)

plt.title('Execution Time Comparison (Log Scale)')
plt.xlabel('Data Size (number of doubles)')
plt.ylabel('Execution Time (μs)')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.savefig('execution_time_comparison.png', dpi=300, bbox_inches='tight')

# 2. 加速比图
plt.figure(figsize=(12, 8))
plt.semilogx(df['Data Size'], df['Two-way Speedup'], 'g-o', label='Two-way Speedup', linewidth=2)
plt.semilogx(df['Data Size'], df['Recursive Speedup'], 'b-o', label='Recursive Speedup', linewidth=2)
plt.semilogx(df['Data Size'], df['In-place Speedup'], 'm-o', label='In-place Speedup', linewidth=2)
plt.axhline(y=1, color='r', linestyle='--', alpha=0.5)  # 基准线 - 无加速

# 添加缓存边界线
plt.axvline(x=l1_size, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=l2_size, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=l3_size, color='gray', linestyle='--', alpha=0.7)

# 标记缓存边界
plt.text(l1_size*1.1, plt.ylim()[0]*1.2, 'L1 Cache', rotation=90, alpha=0.7)
plt.text(l2_size*1.1, plt.ylim()[0]*1.2, 'L2 Cache', rotation=90, alpha=0.7)
plt.text(l3_size*1.1, plt.ylim()[0]*1.2, 'L3 Cache', rotation=90, alpha=0.7)

plt.title('Algorithm Speedup Ratio Compared to Naive Implementation')
plt.xlabel('Data Size (number of doubles)')
plt.ylabel('Speedup Ratio')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.savefig('speedup_comparison.png', dpi=300, bbox_inches='tight')

# 3. 缓存临界区域分析 - 着重展示L1、L2、L3边界附近的加速比变化
# 创建三个子图
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# L1缓存边界区域分析
l1_mask = (df['Data Size'] >= 1000) & (df['Data Size'] <= 10000)
axes[0].plot(df.loc[l1_mask, 'Data Size'], df.loc[l1_mask, 'Two-way Speedup'], 'g-o', label='Two-way')
axes[0].plot(df.loc[l1_mask, 'Data Size'], df.loc[l1_mask, 'Recursive Speedup'], 'b-o', label='Recursive')
axes[0].plot(df.loc[l1_mask, 'Data Size'], df.loc[l1_mask, 'In-place Speedup'], 'm-o', label='In-place')
axes[0].axvline(x=l1_size, color='red', linestyle='--', alpha=0.7)
axes[0].set_title('L1 Cache Boundary (37KB)')
axes[0].set_xlabel('Data Size')
axes[0].set_ylabel('Speedup Ratio')
axes[0].legend()
axes[0].grid(True)

# L2缓存边界区域分析
l2_mask = (df['Data Size'] >= 150000) & (df['Data Size'] <= 600000)
axes[1].plot(df.loc[l2_mask, 'Data Size'], df.loc[l2_mask, 'Two-way Speedup'], 'g-o', label='Two-way')
axes[1].plot(df.loc[l2_mask, 'Data Size'], df.loc[l2_mask, 'Recursive Speedup'], 'b-o', label='Recursive')
axes[1].plot(df.loc[l2_mask, 'Data Size'], df.loc[l2_mask, 'In-place Speedup'], 'm-o', label='In-place')
axes[1].axvline(x=l2_size, color='red', linestyle='--', alpha=0.7)
axes[1].set_title('L2 Cache Boundary (2.67MB)')
axes[1].set_xlabel('Data Size')
axes[1].legend()
axes[1].grid(True)

# L3缓存边界区域分析
l3_mask = (df['Data Size'] >= 3000000) & (df['Data Size'] <= 6000000)
axes[2].plot(df.loc[l3_mask, 'Data Size'], df.loc[l3_mask, 'Two-way Speedup'], 'g-o', label='Two-way')
axes[2].plot(df.loc[l3_mask, 'Data Size'], df.loc[l3_mask, 'Recursive Speedup'], 'b-o', label='Recursive')
axes[2].plot(df.loc[l3_mask, 'Data Size'], df.loc[l3_mask, 'In-place Speedup'], 'm-o', label='In-place')
axes[2].axvline(x=l3_size, color='red', linestyle='--', alpha=0.7)
axes[2].set_title('L3 Cache Boundary (36MB)')
axes[2].set_xlabel('Data Size')
axes[2].legend()
axes[2].grid(True)

plt.tight_layout()
plt.savefig('cache_boundary_analysis.png', dpi=300, bbox_inches='tight')

# 4. 对数-对数刻度下的性能趋势
plt.figure(figsize=(10, 8))

# 创建对数区间，更清晰地显示趋势线
data_sizes = df['Data Size'].values
x_trend = np.logspace(np.log10(min(data_sizes)), np.log10(max(data_sizes)), 100)

# 对每种算法拟合一条趋势线
def fit_power_law(x, y):
    """拟合幂律关系 y = a*x^b"""
    logx = np.log10(x)
    logy = np.log10(y)
    coeffs = np.polyfit(logx, logy, 1)
    return coeffs, 10**coeffs[1] * x_trend**coeffs[0]

# 拟合并绘制
coeffs_naive, trend_naive = fit_power_law(data_sizes, df['Naive Sum (μs)'])
coeffs_two_way, trend_two_way = fit_power_law(data_sizes, df['Two-way Sum (μs)'])
coeffs_recursive, trend_recursive = fit_power_law(data_sizes, df['Recursive Sum (μs)'])
coeffs_inplace, trend_inplace = fit_power_law(data_sizes, df['In-place Sum (μs)'])

plt.loglog(data_sizes, df['Naive Sum (μs)'], 'ro', label='Naive Sum Data')
plt.loglog(x_trend, trend_naive, 'r-', alpha=0.7, linewidth=2, 
           label=f'Naive: O(n^{coeffs_naive[0]:.2f})')

plt.loglog(data_sizes, df['Two-way Sum (μs)'], 'go', label='Two-way Sum Data')
plt.loglog(x_trend, trend_two_way, 'g-', alpha=0.7, linewidth=2, 
           label=f'Two-way: O(n^{coeffs_two_way[0]:.2f})')

plt.loglog(data_sizes, df['Recursive Sum (μs)'], 'bo', label='Recursive Sum Data')
plt.loglog(x_trend, trend_recursive, 'b-', alpha=0.7, linewidth=2, 
           label=f'Recursive: O(n^{coeffs_recursive[0]:.2f})')

plt.loglog(data_sizes, df['In-place Sum (μs)'], 'mo', label='In-place Sum Data')
plt.loglog(x_trend, trend_inplace, 'm-', alpha=0.7, linewidth=2, 
           label=f'In-place: O(n^{coeffs_inplace[0]:.2f})')

plt.title('Algorithm Complexity Analysis (Log-Log Scale)')
plt.xlabel('Data Size (n)')
plt.ylabel('Execution Time (μs)')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.savefig('complexity_analysis.png', dpi=300, bbox_inches='tight')

print("Charts generated:")
print("1. execution_time_comparison.png - Execution time comparison")
print("2. speedup_comparison.png - Speedup ratio comparison")
print("3. cache_boundary_analysis.png - Cache boundary analysis")
print("4. complexity_analysis.png - Complexity analysis")