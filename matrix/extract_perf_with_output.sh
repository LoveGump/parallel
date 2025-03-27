#!/bin/bash

# 输出文件
output_csv="perf_summary_with_output.csv"
echo "program,param,cache-references,cache-misses,output" > "$output_csv"

# 遍历测试的两个程序
for program in naive cache_friendly; do
    for filepath in perf_results/$program/perf_*.txt; do
        # 提取参数值
        filename=$(basename "$filepath")
        param=${filename#perf_}
        param=${param%.txt}

        # 提取 perf 的统计数据
        cache_refs=$(grep "cache-references" "$filepath" | awk '{print $(NF-1)}' | tr -d ',')
        cache_miss=$(grep "cache-misses" "$filepath" | awk '{print $(NF-1)}' | tr -d ',')

        # 默认值设为0
        cache_refs=${cache_refs:-0}
        cache_miss=${cache_miss:-0}

        # 提取程序输出：去掉 perf 输出部分（以 " Performance counter stats" 或 " Performance counter" 开头的行以及之后的内容）
        prog_output=$(awk '/^ Performance counter/{exit} {print}' "$filepath" | tr -d '\n' | sed 's/"/'\''/g')

        # 写入 CSV：输出加引号以防有逗号
        echo "$program,$param,$cache_refs,$cache_miss,\"$prog_output\"" >> "$output_csv"
    done
done

echo "✅ 已生成结构化文件：$output_csv"
