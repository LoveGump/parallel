#!/bin/bash

OUTPUT_DIR="results"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# 编译并运行 x86
echo "编译并运行 x86..."
g++ native.cpp -o native_x86
./native_x86 > "${OUTPUT_DIR}/results_x86_${TIMESTAMP}.txt"
echo "x86结果已保存到: ${OUTPUT_DIR}/results_x86_${TIMESTAMP}.txt"

# 尝试 aarch64 交叉编译并使用 QEMU 运行
if command -v aarch64-linux-gnu-g++ &> /dev/null; then
    echo "编译 aarch64..."
    aarch64-linux-gnu-g++ native.cpp -o native_arm

    if command -v qemu-aarch64 &> /dev/null; then
        echo "运行 aarch64 模拟..."
        qemu-aarch64 -L /usr/aarch64-linux-gnu ./native_arm > "${OUTPUT_DIR}/results_arm_${TIMESTAMP}.txt"
        echo "aarch64结果已保存到: ${OUTPUT_DIR}/results_arm_${TIMESTAMP}.txt"
    else
        echo "未找到 QEMU，请安装: sudo apt-get install qemu-user-static"
    fi
else
    echo "未找到 aarch64 交叉编译器，请安装: sudo apt-get install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu"
fi

echo "完成！"