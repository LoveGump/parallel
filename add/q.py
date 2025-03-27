import os
import csv
import re

def parse_perf_file(file_path):
    # 存储解析后的统计数据 - 增加了cpu_atom相关字段
    stats = {
        'file_name': '',
        # cpu_core统计
        'cpu_core_instructions': 0,
        'cpu_core_cycles': 0,
        'task_clock': 0,
        'cpu_core_cache_references': 0,
        'cpu_core_cache_misses': 0,
        'cpu_core_L1_dcache_load_misses': 0,
        'cpu_core_LLC_load_misses': 0,
        'cpu_time': 0,
        # 新增cpu_atom统计
        'cpu_atom_instructions': 0,
        'cpu_atom_cycles': 0,
        'cpu_atom_cache_references': 0,
        'cpu_atom_cache_misses': 0,
        'cpu_atom_L1_dcache_load_misses': 0,
        'cpu_atom_LLC_load_misses': 0
    }

    # 读取文件并解析
    with open(file_path, 'r') as file:
        content = file.read()
        
        # 提取文件名
        stats['file_name'] = os.path.basename(file_path)
        
        # cpu_core指标解析
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
            
        # 6. L1 数据缓存加载未命中次数
        match = re.search(r'([0-9,]+)\s+cpu_core/L1-dcache-load-misses/', content)
        if match:
            stats['cpu_core_L1_dcache_load_misses'] = int(match.group(1).replace(',', ''))
            
        # 7. LLC 加载未命中次数
        match = re.search(r'([0-9,]+)\s+cpu_core/LLC-load-misses/', content)
        if match:
            stats['cpu_core_LLC_load_misses'] = int(match.group(1).replace(',', ''))
            
        # 8. CPU 时间
        match = re.search(r'([0-9.]+)\s+seconds time elapsed', content)
        if match:
            stats['cpu_time'] = float(match.group(1))

        # cpu_atom指标解析 - 新增
        # 1. CPU Atom 指令数
        match = re.search(r'([0-9,]+)\s+cpu_atom/instructions/', content)
        if match:
            stats['cpu_atom_instructions'] = int(match.group(1).replace(',', ''))
            
        # 2. CPU Atom 周期数
        match = re.search(r'([0-9,]+)\s+cpu_atom/cycles/', content)
        if match:
            stats['cpu_atom_cycles'] = int(match.group(1).replace(',', ''))
            
        # 3. CPU Atom 缓存引用次数
        match = re.search(r'([0-9,]+)\s+cpu_atom/cache-references/', content)
        if match:
            stats['cpu_atom_cache_references'] = int(match.group(1).replace(',', ''))
            
        # 4. CPU Atom 缓存未命中次数
        match = re.search(r'([0-9,]+)\s+cpu_atom/cache-misses/', content)
        if match:
            stats['cpu_atom_cache_misses'] = int(match.group(1).replace(',', ''))
            
        # 5. CPU Atom L1 数据缓存加载未命中次数
        match = re.search(r'([0-9,]+)\s+cpu_atom/L1-dcache-load-misses/', content)
        if match:
            stats['cpu_atom_L1_dcache_load_misses'] = int(match.group(1).replace(',', ''))
            
        # 6. CPU Atom LLC 加载未命中次数
        match = re.search(r'([0-9,]+)\s+cpu_atom/LLC-load-misses/', content)
        if match:
            stats['cpu_atom_LLC_load_misses'] = int(match.group(1).replace(',', ''))

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

def calculate_total_instructions(atom_instr, core_instr):
    return atom_instr + core_instr

def process_perf_data(directory_path):
    all_stats = []
    
    # 遍历目录中的所有 *_perf.txt 文件
    for file_name in os.listdir(directory_path):
        if file_name.endswith('_perf.txt'):
            file_path = os.path.join(directory_path, file_name)
            print(f"Processing file: {file_path}")
            stats = parse_perf_file(file_path)
            
            # 计算性能指标 - core
            stats['core_IPC'] = calculate_ipc(stats['cpu_core_instructions'], stats['cpu_core_cycles'])
            stats['core_Cache_miss_rate'] = calculate_cache_miss_rate(stats['cpu_core_cache_references'], stats['cpu_core_cache_misses'])
            stats['core_L1_miss_rate'] = calculate_l1_miss_rate(stats['cpu_core_cache_references'], stats['cpu_core_L1_dcache_load_misses'])
            stats['core_LLC_miss_rate'] = calculate_llc_miss_rate(stats['cpu_core_cache_references'], stats['cpu_core_LLC_load_misses'])
            
            # 计算性能指标 - atom (新增)
            stats['atom_IPC'] = calculate_ipc(stats['cpu_atom_instructions'], stats['cpu_atom_cycles'])
            stats['atom_Cache_miss_rate'] = calculate_cache_miss_rate(stats['cpu_atom_cache_references'], stats['cpu_atom_cache_misses'])
            stats['atom_L1_miss_rate'] = calculate_l1_miss_rate(stats['cpu_atom_cache_references'], stats['cpu_atom_L1_dcache_load_misses'])
            stats['atom_LLC_miss_rate'] = calculate_llc_miss_rate(stats['cpu_atom_cache_references'], stats['cpu_atom_LLC_load_misses'])
            
            # 计算总指令数
            stats['total_instructions'] = calculate_total_instructions(stats['cpu_atom_instructions'], stats['cpu_core_instructions'])

            all_stats.append(stats)
    
    return all_stats

def save_to_csv(data, output_file):
    # 定义 CSV 字段名称 - 增加了新的字段
    fieldnames = [
        'file_name',
        'total_instructions',
        'cpu_time',
        # Core指标
        'cpu_core_instructions', 
        'cpu_core_cycles',
        'core_IPC',
        'cpu_core_cache_references',
        'cpu_core_cache_misses',
        'core_Cache_miss_rate',
        'cpu_core_L1_dcache_load_misses',
        'core_L1_miss_rate',
        'cpu_core_LLC_load_misses',
        'core_LLC_miss_rate',
        # Atom指标
        'cpu_atom_instructions',
        'cpu_atom_cycles',
        'atom_IPC',
        'cpu_atom_cache_references',
        'cpu_atom_cache_misses',
        'atom_Cache_miss_rate',
        'cpu_atom_L1_dcache_load_misses',
        'atom_L1_miss_rate',
        'cpu_atom_LLC_load_misses',
        'atom_LLC_miss_rate',
        # 其他
        'task_clock'
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
            print(f"Total Instructions: {stat['total_instructions']:,}")
            print(f"CPU Time: {stat['cpu_time']:.6f} seconds")
            
            print(f"\n-- Core Stats --")
            print(f"Core Instructions: {stat['cpu_core_instructions']:,}")
            print(f"Core IPC: {stat['core_IPC']}")
            print(f"Core L1 Cache Miss Rate: {stat['core_L1_miss_rate']*100:.2f}%")
            print(f"Core LLC Cache Miss Rate: {stat['core_LLC_miss_rate']*100:.2f}%")
            
            print(f"\n-- Atom Stats --")
            print(f"Atom Instructions: {stat['cpu_atom_instructions']:,}")
            print(f"Atom IPC: {stat['atom_IPC']}")
            print(f"Atom L1 Cache Miss Rate: {stat['atom_L1_miss_rate']*100:.2f}%")
            print(f"Atom LLC Cache Miss Rate: {stat['atom_LLC_miss_rate']*100:.2f}%")

if __name__ == '__main__':
    main()