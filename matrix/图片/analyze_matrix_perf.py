import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 读取CSV文件
df = pd.read_csv('/home/gump/pall/matrix/matrix_performance.csv')

# 重命名列以便在代码中使用英文列名
df_eng = df.rename(columns={
    '规模': 'size',
    '朴素算法(us)': 'naive_time',
    '优化算法(us)': 'optimized_time',
    '加速比': 'speedup'
})

# 1. 执行时间对比图 (单独的图)
plt.figure(figsize=(10, 6))
plt.plot(df_eng['size'], df_eng['naive_time'], 'r-o', label='Naive Algorithm')
plt.plot(df_eng['size'], df_eng['optimized_time'], 'b-s', label='Optimized Algorithm')
plt.title('Matrix Size vs. Execution Time', fontsize=16)
plt.xlabel('Matrix Size (n)', fontsize=14)
plt.ylabel('Execution Time (us)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# 在关键区域添加标注
special_sizes = [400, 2000, 5000]
for size in special_sizes:
    idx = df_eng[df_eng['size'] == size].index[0]
    plt.annotate(f'n={size}', 
                 xy=(size, df_eng.loc[idx, 'naive_time']),
                 xytext=(size+200, df_eng.loc[idx, 'naive_time']*0.9),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))

plt.tight_layout()
plt.savefig('matrix_execution_time.png', dpi=300)
print("Saved: matrix_execution_time.png")
plt.close()  # 关闭当前图表

# 2. 加速比图 (单独的图)
plt.figure(figsize=(10, 6))
plt.plot(df_eng['size'], df_eng['speedup'], 'g-o', linewidth=2)
plt.title('Matrix Size vs. Speedup Ratio', fontsize=16)
plt.xlabel('Matrix Size (n)', fontsize=14)
plt.ylabel('Speedup Ratio', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# 在加速比图上标注重要转折点
important_points = df_eng[df_eng['speedup'] > df_eng['speedup'].shift(1) * 1.2].index
for i in important_points:
    if i > 0:  # 跳过第一个点
        plt.annotate(f'n={df_eng.loc[i, "size"]}, speedup={df_eng.loc[i, "speedup"]:.2f}',
                     xy=(df_eng.loc[i, 'size'], df_eng.loc[i, 'speedup']),
                     xytext=(df_eng.loc[i, 'size']*0.8, df_eng.loc[i, 'speedup']*1.1),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))

plt.tight_layout()
plt.savefig('matrix_speedup_ratio.png', dpi=300)
print("Saved: matrix_speedup_ratio.png")
plt.close()  # 关闭当前图表

# 3. 对数比例图
plt.figure(figsize=(10, 6))
plt.loglog(df_eng['size'], df_eng['naive_time'], 'r-o', label='Naive Algorithm')
plt.loglog(df_eng['size'], df_eng['optimized_time'], 'b-s', label='Optimized Algorithm')
plt.title('Matrix Size vs. Execution Time (Log Scale)', fontsize=16)
plt.xlabel('Matrix Size (n) - Log Scale', fontsize=14)
plt.ylabel('Execution Time (us) - Log Scale', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, which="both", linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('matrix_performance_log_scale.png', dpi=300)
print("Saved: matrix_performance_log_scale.png")
plt.close()  # 关闭当前图表

# 4. 关键区域的加速比变化
plt.figure(figsize=(10, 6))

# 定义关键区域
key_regions = [
    (0, 100, 'Small Size'),
    (300, 600, 'L1 Cache Boundary'),
    (1500, 3000, 'L3 Cache Boundary'),
    (5000, 9000, 'Large Size')
]

# 设置颜色
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']

# 为每个关键区域绘制不同颜色的加速比
for i, (start, end, label) in enumerate(key_regions):
    mask = (df_eng['size'] >= start) & (df_eng['size'] <= end)
    plt.plot(df_eng.loc[mask, 'size'], df_eng.loc[mask, 'speedup'], 
             'o-', label=label, color=colors[i], linewidth=2)

plt.title('Speedup Ratio in Different Cache Regions', fontsize=16)
plt.xlabel('Matrix Size (n)', fontsize=14)
plt.ylabel('Speedup Ratio', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('matrix_speedup_by_regions.png', dpi=300)
print("Saved: matrix_speedup_by_regions.png")
plt.close()  # 关闭当前图表

print("All chart analysis completed!")