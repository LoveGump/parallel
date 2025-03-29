import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.ticker as ticker

# 设置输出目录
output_dir = 'add/图片/platform_comparison'
os.makedirs(output_dir, exist_ok=True)

# 读取CSV文件
win_file_path = 'd:/my_study_program/code_25Spring/Parallel/add/sum_algorithm_results_win.csv'
linux_file_path = 'd:/my_study_program/code_25Spring/Parallel/add/sum_algorithm_results_linux.csv'

df_win = pd.read_csv(win_file_path)
df_linux = pd.read_csv(linux_file_path)

# 确保两个数据集具有相同的数据大小
common_sizes = sorted(list(set(df_win['数据大小']).intersection(set(df_linux['数据大小']))))
df_win = df_win[df_win['数据大小'].isin(common_sizes)].reset_index(drop=True)
df_linux = df_linux[df_linux['数据大小'].isin(common_sizes)].reset_index(drop=True)

# 设置全局字体和样式
plt.rcParams['font.family'] = 'SimHei'  # 使用中文字体
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.style.use('ggplot')

# 设置缓存边界（以数据元素个数表示）
bytes_per_double = 8
# Windows 机器
win_l1_size = 4600    # L1 缓存大小约37KB，约4600个double
win_l2_size = 330000  # L2 缓存大小约2.67MB，约333K个double
win_l3_size = 4500000 # L3 缓存大小约36MB，约4.5M个double

# Linux 机器 (假设与Windows不同，可以根据实际情况调整)
linux_l1_size = 4600    # 同样假设为4600个double
linux_l2_size = 330000  # 同样假设为333K个double
linux_l3_size = 4500000 # 同样假设为4.5M个double

# 创建图形：各算法在Windows和Linux上的执行时间比较
algorithms = [
    ('平凡算法', '平凡算法(μs)'), 
    ('两路链式', '两路链式(μs)'), 
    ('递归两两相加', '递归两两相加(μs)'),
    ('原地两两相加', '原地两两相加(μs)'),
    ('展开4路', '展开4路(μs)'),
    ('展开8路分块', '展开8路分块(μs)')
]

# 1. 两平台执行时间比较（对数比例尺）
plt.figure(figsize=(18, 12))

# 为每个算法创建子图
for i, (algo_name, algo_col) in enumerate(algorithms):
    ax = plt.subplot(2, 3, i+1)
    
    # 绘制Windows和Linux的执行时间
    ax.loglog(df_win['数据大小'], df_win[algo_col], 'r-o', linewidth=2, markersize=5, label='Windows')
    ax.loglog(df_linux['数据大小'], df_linux[algo_col], 'b-o', linewidth=2, markersize=5, label='Linux')
    
    # 添加Windows的缓存边界线
    ax.axvline(x=win_l1_size, color='r', linestyle='--', alpha=0.3)
    ax.axvline(x=win_l2_size, color='r', linestyle='--', alpha=0.3)
    ax.axvline(x=win_l3_size, color='r', linestyle='--', alpha=0.3)
    
    # 添加Linux的缓存边界线
    ax.axvline(x=linux_l1_size, color='b', linestyle='--', alpha=0.3)
    ax.axvline(x=linux_l2_size, color='b', linestyle='--', alpha=0.3)
    ax.axvline(x=linux_l3_size, color='b', linestyle='--', alpha=0.3)
    
    ax.set_title(f'{algo_name}执行时间比较')
    ax.set_xlabel('数据大小 (元素个数)')
    ax.set_ylabel('执行时间 (微秒)')
    ax.legend()
    ax.grid(True, which="both", ls="-", alpha=0.2)

plt.tight_layout()
plt.suptitle('Windows vs Linux: 各算法执行时间比较', fontsize=16, y=1.02)
plt.savefig(os.path.join(output_dir, '两平台执行时间比较.png'), dpi=300, bbox_inches='tight')

# 2. 计算Linux相对于Windows的性能提升比例
performance_ratio = pd.DataFrame()
performance_ratio['数据大小'] = common_sizes

for _, algo_col in algorithms:
    # 计算Linux相对于Windows的性能比(>1表示Windows更快,<1表示Linux更快)
    performance_ratio[f'{algo_col}_比例'] = df_win[algo_col] / df_linux[algo_col]

# 绘制性能比例图
plt.figure(figsize=(14, 10))
for i, (algo_name, algo_col) in enumerate(algorithms):
    plt.semilogx(
        performance_ratio['数据大小'], 
        performance_ratio[f'{algo_col}_比例'], 
        marker='o', 
        linewidth=2, 
        label=algo_name
    )

# 添加参考线
plt.axhline(y=1.0, color='k', linestyle='--', alpha=0.7)
plt.text(common_sizes[-1]*1.05, 1.0, '性能相等', va='center')

# 添加缓存边界线（假设两个平台缓存大小相同）
plt.axvline(x=win_l1_size, color='gray', linestyle='--', alpha=0.5)
plt.axvline(x=win_l2_size, color='gray', linestyle='--', alpha=0.5)
plt.axvline(x=win_l3_size, color='gray', linestyle='--', alpha=0.5)

plt.title('Windows vs Linux: 执行时间比例 (Windows/Linux)', fontsize=16)
plt.xlabel('数据大小 (元素个数)', fontsize=14)
plt.ylabel('执行时间比例', fontsize=14)
plt.legend(loc='best', fontsize=12)
plt.grid(True, which="both", ls="-", alpha=0.2)

# 标记比例方向
plt.text(common_sizes[0]*0.8, plt.ylim()[1]*0.9, "Windows更慢", fontsize=12)
plt.text(common_sizes[0]*0.8, plt.ylim()[0]*1.1, "Linux更慢", fontsize=12)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '两平台性能比例.png'), dpi=300)

# 3. 比较两个平台上算法的加速比
accelerations = [
    ('两路加速比', '两路加速比'),
    ('递归加速比', '递归加速比'),
    ('两两相加加速比', '两两相加加速比'),
    ('展开4路加速比', '展开4路加速比'),
    ('展开8路加速比', '展开8路加速比')
]

plt.figure(figsize=(18, 12))

for i, (accel_name, accel_col) in enumerate(accelerations):
    ax = plt.subplot(2, 3, i+1)
    
    # 绘制Windows和Linux的加速比
    ax.semilogx(df_win['数据大小'], df_win[accel_col], 'r-o', linewidth=2, markersize=5, label='Windows')
    ax.semilogx(df_linux['数据大小'], df_linux[accel_col], 'b-o', linewidth=2, markersize=5, label='Linux')
    
    # 添加参考线
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.7, label='无加速')
    
    # 添加缓存边界线
    ax.axvline(x=win_l1_size, color='gray', linestyle='--', alpha=0.3)
    ax.axvline(x=win_l2_size, color='gray', linestyle='--', alpha=0.3)
    ax.axvline(x=win_l3_size, color='gray', linestyle='--', alpha=0.3)
    
    ax.set_title(f'{accel_name}对比')
    ax.set_xlabel('数据大小 (元素个数)')
    ax.set_ylabel('加速比')
    ax.legend()
    ax.grid(True, which="both", ls="-", alpha=0.2)

plt.tight_layout()
plt.suptitle('Windows vs Linux: 各算法加速比对比', fontsize=16, y=1.02)
plt.savefig(os.path.join(output_dir, '两平台加速比对比.png'), dpi=300, bbox_inches='tight')

# 4. 对比各算法在两平台上的相对表现（选择几个代表性数据大小）
representative_sizes = [
    1024,    # 小数据集 (L1内)
    65536,   # 中等数据集 (L1-L2间)
    1048576, # 大数据集 (L2-L3间)
    33554432 # 超大数据集 (L3外)
]

# 筛选代表性数据大小
win_rep = df_win[df_win['数据大小'].isin(representative_sizes)].reset_index(drop=True)
linux_rep = df_linux[df_linux['数据大小'].isin(representative_sizes)].reset_index(drop=True)

# 分别绘制各数据规模下的算法比较
plt.figure(figsize=(20, 15))

for i, size in enumerate(representative_sizes):
    ax = plt.subplot(2, 2, i+1)
    
    win_data = win_rep[win_rep['数据大小'] == size]
    linux_data = linux_rep[linux_rep['数据大小'] == size]
    
    # 提取各算法的执行时间
    algo_names = [name for name, _ in algorithms]
    win_times = [win_data[col].values[0] for _, col in algorithms]
    linux_times = [linux_data[col].values[0] for _, col in algorithms]
    
    # 计算比例
    ratios = [w/l for w, l in zip(win_times, linux_times)]
    
    # 绘制柱状图
    x = np.arange(len(algo_names))
    width = 0.35
    
    ax.bar(x - width/2, win_times, width, label='Windows', color='lightcoral')
    ax.bar(x + width/2, linux_times, width, label='Linux', color='lightskyblue')
    
    # 添加比例标签
    for j, ratio in enumerate(ratios):
        ax.text(j, max(win_times[j], linux_times[j])*1.05, 
               f'Win/Linux={ratio:.2f}', 
               ha='center', va='bottom', 
               rotation=0, fontsize=9)
    
    ax.set_yscale('log')
    ax.set_ylabel('执行时间 (微秒)')
    ax.set_title(f'数据大小: {size} 元素')
    ax.set_xticks(x)
    ax.set_xticklabels(algo_names, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, which='both', axis='y', alpha=0.3)

plt.tight_layout()
plt.suptitle('Windows vs Linux: 不同数据规模下的算法性能对比', fontsize=16, y=1.02)
plt.savefig(os.path.join(output_dir, '两平台数据规模性能对比.png'), dpi=300, bbox_inches='tight')

# 5. 各算法在两平台上的最大加速比对比
max_speedup_win = pd.DataFrame({
    '算法': [name for name, _ in accelerations],
    '最大加速比': [df_win[col].max() for _, col in accelerations],
    '达到最大值的数据大小': [df_win.loc[df_win[col].idxmax(), '数据大小'] for _, col in accelerations]
})

max_speedup_linux = pd.DataFrame({
    '算法': [name for name, _ in accelerations],
    '最大加速比': [df_linux[col].max() for _, col in accelerations],
    '达到最大值的数据大小': [df_linux.loc[df_linux[col].idxmax(), '数据大小'] for _, col in accelerations]
})

# 保存为CSV
max_speedup_win.to_csv(os.path.join(output_dir, 'windows_max_speedup.csv'), index=False)
max_speedup_linux.to_csv(os.path.join(output_dir, 'linux_max_speedup.csv'), index=False)

# 绘制最大加速比对比图
plt.figure(figsize=(12, 8))
x = np.arange(len(accelerations))
width = 0.35

plt.bar(x - width/2, max_speedup_win['最大加速比'], width, label='Windows', color='lightcoral')
plt.bar(x + width/2, max_speedup_linux['最大加速比'], width, label='Linux', color='lightskyblue')

# 添加标签
for i, v in enumerate(max_speedup_win['最大加速比']):
    plt.text(i - width/2, v + 0.1, f'{v:.2f}', ha='center')
    
for i, v in enumerate(max_speedup_linux['最大加速比']):
    plt.text(i + width/2, v + 0.1, f'{v:.2f}', ha='center')

plt.ylabel('最大加速比')
plt.title('Windows vs Linux: 各算法最大加速比对比')
plt.xticks(x, [name for name, _ in accelerations], rotation=45, ha='right')
plt.legend()
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '最大加速比对比.png'), dpi=300)

print(f"对比分析图表已生成到目录: {output_dir}")
print("生成的图表包括:")
print("1. 两平台执行时间比较.png - 各算法在Windows和Linux上的执行时间对比")
print("2. 两平台性能比例.png - Windows执行时间与Linux执行时间的比例")
print("3. 两平台加速比对比.png - 各优化算法在两个平台上的加速比对比")
print("4. 两平台数据规模性能对比.png - 不同数据规模下各算法在两平台上的性能")
print("5. 最大加速比对比.png - 各算法在两平台上能达到的最大加速比")
print("6. windows_max_speedup.csv 和 linux_max_speedup.csv - 记录了各算法的最大加速比数据")