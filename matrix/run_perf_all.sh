#!/bin/bash

# 参数列表
params=(10 20 30 50 70 100 200 400 450 500 550 600 700 800 900 1000 1300 1400 1500 1600 1700 1800 1900 2000 2200 3000 4000 )

# 要测试的程序
PROGRAM="./common"

# 创建结果文件
RESULTS_CSV="common.csv"

# 写入CSV表头
echo "规模,朴素算法(us),优化算法(us),加速比" > $RESULTS_CSV

# 显示进度条函数
progress() {
    local current=$1
    local total=$2
    local width=50
    local percent=$((current * 100 / total))
    local completed=$((width * current / total))
    local remaining=$((width - completed))
    
    printf "\r["
    printf "%${completed}s" | tr ' ' '#'
    printf "%${remaining}s" | tr ' ' ' '
    printf "] %3d%% (%d/%d)" $percent $current $total
}

total=${#params[@]}
count=0

echo "📊 开始收集所有规模的测试结果..."

for param in "${params[@]}"; do
    count=$((count + 1))
    progress $count $total
    
    # 运行程序并提取结果
    output=$($PROGRAM $param)
    
    # 提取朴素算法时间
    naive_time=$(echo "$output" | grep "平均时间:" | head -1 | awk '{print $2}')
    
    # 提取优化算法时间
    opt_time=$(echo "$output" | grep "平均时间:" | tail -1 | awk '{print $2}')
    
    # 提取加速比
    speedup=$(echo "$output" | grep "加速比" | awk '{print $2}' | sed 's/x//')
    
    # 将结果写入CSV
    echo "$param,$naive_time,$opt_time,$speedup" >> $RESULTS_CSV
done

echo -e "\n✅ 所有测试完成！结果已保存到 $RESULTS_CSV"