import os
import csv
import re

def parse_perf_file(file_path):
    # 存储解析后的统计数据 - 增加了新的字段
    stats = {
        'file_name': '',
        'cpu_core_instructions': 0,
        'cpu_core_cycles': 0,
        'task_clock': 0,
        'cpu_core_cache_references': 0,
        'cpu_core_cache_misses': 0,
        'cpu_core_L1_dcache_load_misses': 0,  # 新增
        'cpu_core_LLC_load_misses': 0,        # 新增
        'cpu_time': 0                         # 新增
    }

    # 读取文件并解析
    with open(file_path, 'r') as file:
        content = file.read()
        
        # 提取文件名
        stats['file_name'] = os.path.basename(file_path)
        
        # 使用正则表达式更精确地提取数值
        # 1. CPU 指令数
        match = re.search(r'([0-9,]+)\s+cpu_core/instructions/', content)
        if match:
            stats['cpu_core_instructions'] = int(match.group(1).replace(',', ''))
            
        # 2. CPU 周期数
        match = re.search(r'([0-9,]+)\s+cpu_core/cycles/', content)
        if match:
            stats['cpu_core_cycles'] = int(match.group(1).replace(',', ''))
            
        # 3. 任务时钟时间
        match = re.search(r'([0-9.]+)\s+msec\s+task-clock', content)
        if match:
            stats['task_clock'] = float(match.group(1))
            
        # 4. 缓存引用次数
        match = re.search(r'([0-9,]+)\s+cpu_core/cache-references/', content)
        if match:
            stats['cpu_core_cache_references'] = int(match.group(1).replace(',', ''))
            
        # 5. 缓存未命中次数
        match = re.search(r'([0-9,]+)\s+cpu_core/cache-misses/', content)
        if match:
            stats['cpu_core_cache_misses'] = int(match.group(1).replace(',', ''))
            
        # 6. L1 数据缓存加载未命中次数（新增）
        match = re.search(r'([0-9,]+)\s+cpu_core/L1-dcache-load-misses/', content)
        if match:
            stats['cpu_core_L1_dcache_load_misses'] = int(match.group(1).replace(',', ''))
            
        # 7. LLC 加载未命中次数（新增）
        match = re.search(r'([0-9,]+)\s+cpu_core/LLC-load-misses/', content)
        if match:
            stats['cpu_core_LLC_load_misses'] = int(match.group(1).replace(',', ''))
            
        # 8. CPU 时间（新增 - 从time elapsed提取）
        match = re.search(r'([0-9.]+)\s+seconds time elapsed', content)
        if match:
            stats['cpu_time'] = float(match.group(1))

    return stats

def calculate_ipc(instructions, cycles):
    if cycles == 0:
        return 0
    return round(instructions / cycles, 4)  # 保留4位小数

def calculate_cache_miss_rate(cache_references, cache_misses):
    if cache_references == 0:
        return 0
    return round(cache_misses / cache_references, 4)  # 保留4位小数

def calculate_l1_miss_rate(cache_references, l1_misses):
    if cache_references == 0:
        return 0
    return round(l1_misses / cache_references, 4)  # 保留4位小数

def calculate_llc_miss_rate(cache_references, llc_misses):
    if cache_references == 0:
        return 0
    return round(llc_misses / cache_references, 4)  # 保留4位小数

def process_perf_data(directory_path):
    all_stats = []
    
    # 遍历目录中的所有 *_perf.txt 文件
    for file_name in os.listdir(directory_path):
        if file_name.endswith('_perf.txt'):
            file_path = os.path.join(directory_path, file_name)
            print(f"Processing file: {file_path}")
            stats = parse_perf_file(file_path)
            
            # 计算性能指标
            stats['IPC'] = calculate_ipc(stats['cpu_core_instructions'], stats['cpu_core_cycles'])
            stats['Cache_miss_rate'] = calculate_cache_miss_rate(stats['cpu_core_cache_references'], stats['cpu_core_cache_misses'])
            stats['L1_miss_rate'] = calculate_l1_miss_rate(stats['cpu_core_cache_references'], stats['cpu_core_L1_dcache_load_misses'])
            stats['LLC_miss_rate'] = calculate_llc_miss_rate(stats['cpu_core_cache_references'], stats['cpu_core_LLC_load_misses'])

            all_stats.append(stats)
    
    return all_stats

def save_to_csv(data, output_file):
    # 定义 CSV 字段名称 - 增加了新的字段
    fieldnames = [
        'file_name',
        'cpu_core_instructions', 
        'cpu_core_cycles',
        'task_clock',
        'cpu_time',  # 新增
        'IPC',
        'cpu_core_cache_references',
        'cpu_core_cache_misses',
        'Cache_miss_rate',
        'cpu_core_L1_dcache_load_misses',  # 新增
        'L1_miss_rate',  # 新增
        'cpu_core_LLC_load_misses',  # 新增
        'LLC_miss_rate'  # 新增
    ]
    
    # 将数据写入 CSV 文件
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # 写入标题行
        writer.writeheader()
        
        # 写入每行数据
        for row in data:
            writer.writerow(row)

def main():
    # 设置数据文件所在的目录
    directory_path = './'  # 这里请替换为实际的文件夹路径
    
    # 处理数据
    stats = process_perf_data(directory_path)
    
    # 保存为 CSV 文件
    output_file = './perf_data_complete.csv'
    save_to_csv(stats, output_file)
    print(f"Data has been saved to {output_file}")
    
    # 打印数据摘要
    if stats:
        print("\n===== Performance Data Summary =====")
        for stat in stats:
            print(f"\nFile: {stat['file_name']}")
            print(f"Instructions: {stat['cpu_core_instructions']:,}")
            print(f"Cycles: {stat['cpu_core_cycles']:,}")
            print(f"IPC: {stat['IPC']}")
            print(f"CPU Time: {stat['cpu_time']:.6f} seconds")
            print(f"L1 Cache Miss Rate: {stat['L1_miss_rate']*100:.2f}%")
            print(f"LLC Cache Miss Rate: {stat['LLC_miss_rate']*100:.2f}%")
            print(f"Overall Cache Miss Rate: {stat['Cache_miss_rate']*100:.2f}%")

if __name__ == '__main__':
    main()