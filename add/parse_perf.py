import re
import glob
import csv

def parse_value(val):
    try:
        return float(val.replace(",", "").strip())
    except ValueError:
        return 0

def extract_data(file):
    data = {
        "program": file.replace("_perf.txt", ""),
        "instructions": 0,
        "cycles": 0,
        "task_clock": 0,
        "cache_references": 0,
        "cache_misses": 0,
        "L1_misses": 0,
        "L3_misses": 0
    }

    with open(file) as f:
        for line in f:
            if 'instructions' in line:
                data['instructions'] += parse_value(line.split()[0])
            elif re.search(r'\bcpu_.*?/cycles/', line):
                data['cycles'] += parse_value(line.split()[0])
            elif 'task-clock' in line:
                data['task_clock'] += parse_value(line.split()[0])
            elif 'cache-references' in line:
                data['cache_references'] += parse_value(line.split()[0])
            elif 'cache-misses' in line:
                data['cache_misses'] += parse_value(line.split()[0])
            elif 'L1-dcache-load-misses' in line:
                data['L1_misses'] += parse_value(line.split()[0])
            elif 'LLC-load-misses' in line:
                data['L3_misses'] += parse_value(line.split()[0])

    return data

def compute_metrics(d):
    instructions = d["instructions"]
    cycles = d["cycles"]
    clock_ms = d["task_clock"]
    cref = d["cache_references"]
    cmiss = d["cache_misses"]
    l1miss = d["L1_misses"]
    l3miss = d["L3_misses"]
    l2miss = cmiss - l3miss if cmiss >= l3miss else 0

    metrics = {
        "Program": d["program"],
        "Instructions": int(instructions),
        "CPU 时间 (s)": round(clock_ms / 1000, 6),
        "Parallelism": round(instructions / clock_ms, 4) if clock_ms else "N/A",
        "CPI": round(cycles / instructions, 4) if instructions else "N/A",
        "L1miss": int(l1miss),
        "L2miss": int(l2miss),
        "L3miss": int(l3miss),
        "L1命中率": round(1 - (l1miss / cref), 4) if cref else "N/A",
        "L2命中率": round(1 - (l2miss / cmiss), 4) if cmiss else "N/A",
        "L3命中率": round(1 - (l3miss / cmiss), 4) if cmiss else "N/A",
    }

    return metrics

def main():
    files = glob.glob("*_perf.txt")
    all_metrics = []

    for file in files:
        data = extract_data(file)
        metrics = compute_metrics(data)
        all_metrics.append(metrics)

    # 打印结果
    for m in all_metrics:
        print(m)

    # 保存为 CSV
    keys = list(all_metrics[0].keys())
    with open("perf_summary.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_metrics)

    print("\n✅ 结果已保存为 perf_summary.csv")

if __name__ == "__main__":
    main()
