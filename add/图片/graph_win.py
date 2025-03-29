import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 设置输出目录
output_dir = 'd:/my_study_program/code_25Spring/Parallel/add/图片/output'
os.makedirs(output_dir, exist_ok=True)

# 读取CSV文件
file_path = 'd:/my_study_program/code_25Spring/Parallel/add/sum_algorithm_results_win.csv'
df = pd.read_csv(file_path)

# 设置全局字体和样式
plt.rcParams['font.family'] = 'SimHei'  # 使用中文字体
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.style.use('ggplot')

# 设置缓存边界（以数据元素个数表示）
bytes_per_double = 8
l1_size = 4600    # L1 缓存大小约37KB，约4600个double
l2_size = 330000  # L2 缓存大小约2.67MB，约333K个double
l3_size = 4500000 # L3 缓存大小约36MB，约4.5M个double

# 1. 执行时间比较图 (对数尺度)
plt.figure(figsize=(14, 10))
plt.loglog(df['数据大小'], df['平凡算法(μs)'], 'ro-', label='平凡算法', linewidth=2, markersize=8)
plt.loglog(df['数据大小'], df['两路链式(μs)'], 'go-', label='两路链式', linewidth=2, markersize=8)
plt.loglog(df['数据大小'], df['递归两两相加(μs)'], 'bo-', label='递归两两相加', linewidth=2, markersize=8)
plt.loglog(df['数据大小'], df['原地两两相加(μs)'], 'mo-', label='原地两两相加', linewidth=2, markersize=8)
plt.loglog(df['数据大小'], df['展开4路(μs)'], 'co-', label='展开4路', linewidth=2, markersize=8)
plt.loglog(df['数据大小'], df['展开8路分块(μs)'], 'yo-', label='展开8路分块', linewidth=2, markersize=8)

# 添加缓存边界线
plt.axvline(x=l1_size, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=l2_size, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=l3_size, color='gray', linestyle='--', alpha=0.7)

# 标记缓存边界
ymin, ymax = plt.ylim()
plt.text(l1_size*1.1, ymin*2, 'L1缓存 (37KB)', rotation=90, alpha=0.8)
plt.text(l2_size*1.1, ymin*2, 'L2缓存 (2.67MB)', rotation=90, alpha=0.8)
plt.text(l3_size*1.1, ymin*2, 'L3缓存 (36MB)', rotation=90, alpha=0.8)

plt.title('各算法执行时间比较 (对数尺度)', fontsize=16)
plt.xlabel('数据大小 (double元素个数)', fontsize=14)
plt.ylabel('执行时间 (微秒)', fontsize=14)
plt.legend(loc='upper left', fontsize=12)
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '执行时间比较.png'), dpi=300)

# 2. 加速比图
plt.figure(figsize=(14, 10))
plt.semilogx(df['数据大小'], df['两路加速比'], 'g-o', label='两路链式加速比', linewidth=2, markersize=8)
plt.semilogx(df['数据大小'], df['递归加速比'], 'b-o', label='递归加速比', linewidth=2, markersize=8)
plt.semilogx(df['数据大小'], df['两两相加加速比'], 'm-o', label='原地两两相加加速比', linewidth=2, markersize=8)
plt.semilogx(df['数据大小'], df['展开4路加速比'], 'c-o', label='展开4路加速比', linewidth=2, markersize=8)
plt.semilogx(df['数据大小'], df['展开8路加速比'], 'y-o', label='展开8路加速比', linewidth=2, markersize=8)
plt.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='基准线(无加速)')

# 添加缓存边界线
plt.axvline(x=l1_size, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=l2_size, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=l3_size, color='gray', linestyle='--', alpha=0.7)

# 标记缓存边界
ymin, ymax = plt.ylim()
plt.text(l1_size*1.1, ymin*1.2, 'L1缓存 (37KB)', rotation=90, alpha=0.8)
plt.text(l2_size*1.1, ymin*1.2, 'L2缓存 (2.67MB)', rotation=90, alpha=0.8)
plt.text(l3_size*1.1, ymin*1.2, 'L3缓存 (36MB)', rotation=90, alpha=0.8)

plt.title('各算法相对于平凡算法的加速比', fontsize=16)
plt.xlabel('数据大小 (double元素个数)', fontsize=14)
plt.ylabel('加速比', fontsize=14)
plt.legend(loc='best', fontsize=12)
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '加速比比较.png'), dpi=300)

# 3. 按缓存层次区分的性能趋势图
# 选择几个代表性的数据点
cache_points = [
    # L1内
    1024, 4000,  
    # L1-L2之间
    8192, 65536,  
    # L2-L3之间
    524288, 1048576,  
    # L3外
    8388608, 33554432, 67108864
]

# 筛选特定数据大小的行
selected_df = df[df['数据大小'].isin(cache_points)]

# 数据分组标签
labels = [
    "1K\n(L1内)", "4K\n(L1内)", 
    "8K\n(L1-L2)", "64K\n(L1-L2)", 
    "512K\n(L2-L3)", "1M\n(L2-L3)", 
    "8M\n(L3外)", "32M\n(L3外)", "64M\n(L3外)"
]

# 获取在这些数据点上各算法的时间
fig, ax = plt.subplots(figsize=(16, 10))

# 提取各算法在各数据大小下的性能数据
data_points = selected_df.index
x = np.arange(len(labels))  # x轴位置
width = 0.13  # 柱状图宽度

# 绘制柱状图
rects1 = ax.bar(x - width*2.5, selected_df['平凡算法(μs)'], width, label='平凡算法', color='red')
rects2 = ax.bar(x - width*1.5, selected_df['两路链式(μs)'], width, label='两路链式', color='green')
rects3 = ax.bar(x - width*0.5, selected_df['递归两两相加(μs)'], width, label='递归两两相加', color='blue')
rects4 = ax.bar(x + width*0.5, selected_df['原地两两相加(μs)'], width, label='原地两两相加', color='magenta')
rects5 = ax.bar(x + width*1.5, selected_df['展开4路(μs)'], width, label='展开4路', color='cyan')
rects6 = ax.bar(x + width*2.5, selected_df['展开8路分块(μs)'], width, label='展开8路分块', color='yellow')

# 添加图形元素
ax.set_title('不同缓存级别下各算法性能对比', fontsize=16)
ax.set_xlabel('数据大小 (单位: 元素个数)', fontsize=14)
ax.set_ylabel('执行时间 (微秒)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='upper left', fontsize=12)

# 使用对数尺度
ax.set_yscale('log')

# 添加水平网格线
ax.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '缓存层次性能对比.png'), dpi=300)

# 输出完成信息
print(f"图表已生成到目录: {output_dir}")
print("1. 执行时间比较.png - 各算法执行时间对比 (对数尺度)")
print("2. 加速比比较.png - 各算法相对于平凡算法的加速比")
print("3. 缓存层次性能对比.png - 不同缓存级别下各算法性能对比")