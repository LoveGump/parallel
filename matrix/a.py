import os
import re
import csv

# 设置路径（替换为你本地路径）
data_dir = "/home/gump/pall/matrix/perf_results/cache_friendly"
output_csv = "summary_speedup.csv"

# 正则表达式匹配
re_naive = re.compile(r"Naive\s+算法统计\s*===\s*平均时间:?\s*([0-9.]+)\s*us", re.DOTALL)
re_opt = re.compile(r"优化算法统计\s*===\s*平均时间:?\s*([0-9.]+)\s*us", re.DOTALL)
re_speedup = re.compile(r"加速比\(Naive/Optimized\):\s*([0-9.]+)x", re.DOTALL)
re_scale = re.compile(r"cache_friendly\s+(\d+)[^\d]?")  # 从命令行参数中提规模

rows = []

for filename in sorted(os.listdir(data_dir)):
    if filename.startswith("perf_") and filename.endswith(".txt"):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 从文件内容中提取
        naive_time = float(m.group(1)) if (m := re_naive.search(content)) else None
        opt_time = float(m.group(1)) if (m := re_opt.search(content)) else None
        speedup = float(m.group(1)) if (m := re_speedup.search(content)) else (
            round(naive_time / opt_time, 2) if naive_time and opt_time else None
        )
        scale = int(m.group(1)) if (m := re_scale.search(content)) else None

        if scale:
            rows.append({
                "scale": scale,
                "naive_time_us": naive_time,
                "optimized_time_us": opt_time,
                "speedup": speedup
            })

# 写入 CSV 文件
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ 提取完成，共处理 {len(rows)} 个文件，已保存到 {output_csv}")
