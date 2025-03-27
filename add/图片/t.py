import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取CSV文件 - 确保文件名称正确
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
bytes_per_double = 8
l1_size_bytes = (896 * 1024) / 24
l1_size = int(l1_size_bytes / bytes_per_double)
l2_size_bytes = (32 * 1024 * 1024) / 12
l2_size = int(l2_size_bytes / bytes_per_double)
l3_size_bytes = 36 * 1024 * 1024
l3_size = int(l3_size_bytes / bytes_per_double)

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

print("Charts generated:")
print("1. execution_time_comparison.png - Execution time comparison")
print("2. speedup_comparison.png - Speedup ratio comparison")