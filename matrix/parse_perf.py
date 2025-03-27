import os
import csv

def parse_perf_file(file_path):
    # 存储解析后的统计数据
    stats = {
        'file_name': '',
        'cpu_core_instructions': 0,
        'cpu_core_cycles': 0,
        'task_clock': 0,
        'cpu_core_cache_references': 0,
        'cpu_core_cache_misses': 0,
    }

    # 读取文件并解析
    with open(file_path, 'r') as file:
        for line in file:
            if 'cpu_core/instructions' in line:
                stats['cpu_core_instructions'] = int(line.split()[0].replace(',', ''))
            elif 'cpu_core/cycles' in line:
                stats['cpu_core_cycles'] = int(line.split()[0].replace(',', ''))
            elif 'task-clock' in line:
                stats['task_clock'] = float(line.split()[0].replace(',', ''))
            elif 'cpu_core/cache-references' in line:
                stats['cpu_core_cache_references'] = int(line.split()[0].replace(',', ''))
            elif 'cpu_core/cache-misses' in line:
                stats['cpu_core_cache_misses'] = int(line.split()[0].replace(',', ''))

    return stats

def calculate_ipc(instructions, cycles):
    if cycles == 0:
        return 0
    return round(instructions / cycles, 4)  # 保留4位小数

def calculate_cache_miss_rate(cache_references, cache_misses):
    if cache_references == 0:
        return 0
    return round(cache_misses / cache_references,4)

def process_perf_data(directory_path):
    all_stats = []
    
    # 遍历目录中的所有 *_perf.txt 文件
    for file_name in os.listdir(directory_path):
        if file_name.endswith('_perf.txt'):
            file_path = os.path.join(directory_path, file_name)
            print(f"Processing file: {file_path}")
            stats = parse_perf_file(file_path)
            stats['file_name'] = file_name  # 添加文件名

            # 计算 IPC 和 Cache 读取失败率
            stats['IPC'] = calculate_ipc(stats['cpu_core_instructions'], stats['cpu_core_cycles'])
            stats['Cache_miss_rate'] = calculate_cache_miss_rate(stats['cpu_core_cache_references'], stats['cpu_core_cache_misses'])

            all_stats.append(stats)
    
    return all_stats

def save_to_csv(data, output_file):
    # 定义 CSV 字段名称
    fieldnames = [
        'file_name', 'cpu_core_instructions', 'cpu_core_cycles', 
        'task_clock', 'IPC', 'Cache_miss_rate', 'cpu_core_cache_references', 
        'cpu_core_cache_misses'
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
    output_file = './core_perf_data.csv'
    save_to_csv(stats, output_file)
    print(f"Data has been saved to {output_file}")

if __name__ == '__main__':
    main()
