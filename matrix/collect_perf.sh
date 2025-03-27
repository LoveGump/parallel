#!/bin/bash

# 更通用的事件组合
EVENTS="instructions,cycles,task-clock,cache-references,cache-misses,L1-dcache-load-misses,LLC-load-misses"

PROGRAMS=("native" "cache_friendly")

for prog in "${PROGRAMS[@]}"; do
    if [[ -x "./$prog" ]]; then
        echo "正在收集 $prog 的性能数据..."
        perf stat -e $EVENTS -o "${prog}_perf.txt" ./$prog
        echo "$prog 数据已保存到 ${prog}_perf.txt"
    else
        echo "警告：找不到可执行文件 $prog 或其不可执行"
    fi
done
