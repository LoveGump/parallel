import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 读取CSV文件
df = pd.read_csv('/home/gump/pall/add/perf_data_complete.csv')

# 设置更好的算法名称用于显示
algorithm_names = {
    'recursive_perf.txt': 'Recursive Sum',
    'native_perf.txt': 'Naive Sum',
    'two_way_perf.txt': 'Two-way Sum',
    'eight_perf.txt': '8-way Sum',
    'inplace_perf.txt': 'In-place Sum',
    'four_perf.txt': '4-way Sum'
}

# 添加算法名称列
df['algorithm'] = df['file_name'].apply(lambda x: algorithm_names.get(x, x))

# 按CPU时间排序
df = df.sort_values('cpu_time')

# 设置颜色方案
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# 创建输出目录
os.makedirs('performance_charts', exist_ok=True)

# 设置全局字体和风格
plt.rcParams['font.size'] = 12
plt.style.use('seaborn-v0_8-whitegrid')

# ========== 1. 执行时间对比图 ==========
plt.figure(figsize=(12, 7))
bars = plt.bar(df['algorithm'], df['cpu_time'] * 1000, color=colors)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height:.2f}', ha='center', va='bottom')

plt.title('Algorithm Execution Time Comparison', fontsize=16)
plt.xlabel('Algorithm', fontsize=14)
plt.ylabel('Time (ms)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('performance_charts/execution_time.png', dpi=300)
plt.close()

# ========== 2. 总指令数对比图 ==========
plt.figure(figsize=(12, 7))
bars = plt.bar(df['algorithm'], df['total_instructions']/1e6, color=colors)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.2,
             f'{height:.1f}M', ha='center', va='bottom')

plt.title('Total Instructions Executed', fontsize=16)
plt.xlabel('Algorithm', fontsize=14)
plt.ylabel('Instructions (millions)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('performance_charts/total_instructions.png', dpi=300)
plt.close()

# ========== 3. IPC (每周期指令数) 对比图 ==========
plt.figure(figsize=(12, 7))

# 为Core和Atom分别创建柱状图
x = np.arange(len(df['algorithm']))
width = 0.35

plt.bar(x - width/2, df['core_IPC'], width, label='Core IPC', color='#1f77b4')
plt.bar(x + width/2, df['atom_IPC'], width, label='Atom IPC', color='#ff7f0e')

plt.title('Instructions Per Cycle (IPC) Comparison', fontsize=16)
plt.xlabel('Algorithm', fontsize=14)
plt.ylabel('IPC', fontsize=14)
plt.xticks(x, df['algorithm'], rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('performance_charts/ipc_comparison.png', dpi=300)
plt.close()

# ========== 4. 缓存性能对比图 ==========
plt.figure(figsize=(12, 7))

# 创建分组条形图
bar_width = 0.2
index = np.arange(len(df['algorithm']))

# L1缓存未命中率
plt.bar(index - bar_width, df['core_L1_miss_rate']*100, bar_width, 
        label='L1 Miss Rate (%)', color='#1f77b4')

# 总缓存未命中率
plt.bar(index, df['core_Cache_miss_rate']*100, bar_width, 
        label='Overall Cache Miss Rate (%)', color='#ff7f0e')

# LLC缓存未命中率
plt.bar(index + bar_width, df['core_LLC_miss_rate']*100, bar_width, 
        label='LLC Miss Rate (%)', color='#2ca02c')

plt.title('Cache Performance Comparison (Core)', fontsize=16)
plt.xlabel('Algorithm', fontsize=14)
plt.ylabel('Miss Rate (%)', fontsize=14)
plt.xticks(index, df['algorithm'], rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('performance_charts/cache_performance.png', dpi=300)
plt.close()

# ========== 5. 性能效率对比图 ==========
plt.figure(figsize=(12, 7))

# 计算每个算法的性能效率 (1/时间)
df['performance_efficiency'] = 1 / df['cpu_time']
df['normalized_efficiency'] = df['performance_efficiency'] / df['performance_efficiency'].max()

bars = plt.bar(df['algorithm'], df['normalized_efficiency']*100, color=colors)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{height:.1f}%', ha='center', va='bottom')

plt.title('Normalized Performance Efficiency', fontsize=16)
plt.xlabel('Algorithm', fontsize=14)
plt.ylabel('Efficiency (%)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, 110)  # 设置y轴范围，留出标签空间
plt.tight_layout()
plt.savefig('performance_charts/performance_efficiency.png', dpi=300)
plt.close()

# ========== 6. 综合比较雷达图 ==========
plt.figure(figsize=(10, 10))

# 选择要在雷达图中显示的指标
metrics = ['Performance', 'Core IPC', 'Atom IPC', 'L1 Cache', 'LLC Cache']
max_vals = {
    'Performance': 1/df['cpu_time'].min(),  # 性能 = 1/时间
    'Core IPC': df['core_IPC'].max(),
    'Atom IPC': df['atom_IPC'].max(),
    'L1 Cache': 1 - df['core_L1_miss_rate'].min(),  # 命中率 = 1 - 未命中率
    'LLC Cache': 1 - df['core_LLC_miss_rate'].min()
}

# 准备雷达图数据
angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]  # 闭合多边形

# 雷达图轴标签位置
ax = plt.subplot(111, polar=True)
plt.xticks(angles[:-1], metrics, fontsize=12)

# 遍历每个算法
for i, (idx, row) in enumerate(df.iterrows()):
    values = [
        1/row['cpu_time']/max_vals['Performance'],
        row['core_IPC']/max_vals['Core IPC'],
        row['atom_IPC']/max_vals['Atom IPC'],
        (1-row['core_L1_miss_rate'])/(1-df['core_L1_miss_rate'].min()),
        (1-row['core_LLC_miss_rate'])/(1-df['core_LLC_miss_rate'].min())
    ]
    values += values[:1]  # 闭合多边形
    
    # 绘制雷达图
    ax.plot(angles, values, linewidth=2, label=row['algorithm'], color=colors[i%len(colors)])
    ax.fill(angles, values, alpha=0.1, color=colors[i%len(colors)])

# 配置雷达图
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.title('Algorithm Performance Radar Chart', fontsize=16, pad=20)
plt.tight_layout()
plt.savefig('performance_charts/radar_chart.png', dpi=300)
plt.close()

print("所有图表已生成在 performance_charts 目录中")