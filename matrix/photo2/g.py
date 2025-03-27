import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Read CSV file
df = pd.read_csv('/home/gump/pall/matrix/matrix_performance_results.csv')

# Rename columns 
df_eng = df.rename(columns={
    '规模': 'size',
    '朴素算法(us)': 'naive_time',
    '优化算法(us)': 'optimized_time',
    '加速比': 'speedup'
})

# Calculate memory requirements
df_eng['memory_bytes'] = df_eng['size'].apply(lambda n: (n*n*8) + (n*8) + (n*8))
df_eng['memory_MB'] = df_eng['memory_bytes'] / (1024*1024)

# CPU cache information
L1d_size_per_core = 896 / 24  # KB (~37.33KB)
L2_size_per_unit = 32 / 12    # MB (~2.67MB)
L3_size_total = 36           # MB

# Calculate matrix dimensions at cache boundaries
L1d_matrix_dim = int(np.sqrt((L1d_size_per_core * 1024) / 8))
L2_matrix_dim = int(np.sqrt((L2_size_per_unit * 1024 * 1024) / 8))
L3_matrix_dim = int(np.sqrt((L3_size_total * 1024 * 1024) / 8))

# Find best speedup
best_speedup_idx = df_eng['speedup'].idxmax()
best_speedup = df_eng.loc[best_speedup_idx, 'speedup']
best_size = df_eng.loc[best_speedup_idx, 'size']

# =========== Chart 1: Execution Time ===========
plt.figure(figsize=(12, 7))
plt.plot(df_eng['size'], df_eng['naive_time'], 'r-o', label='Naive Algorithm (Column-first)', linewidth=2, markersize=7)
plt.plot(df_eng['size'], df_eng['optimized_time'], 'b-s', label='Cache-friendly Algorithm (Row-first)', linewidth=2, markersize=7)

# Add cache boundary lines
plt.axvline(x=L1d_matrix_dim, color='gray', linestyle='--', alpha=0.7, label=f'L1d Cache (~{L1d_matrix_dim}×{L1d_matrix_dim})')
plt.axvline(x=L2_matrix_dim, color='gray', linestyle=':', alpha=0.7, label=f'L2 Cache (~{L2_matrix_dim}×{L2_matrix_dim})')
plt.axvline(x=L3_matrix_dim, color='gray', linestyle='-.', alpha=0.7, label=f'L3 Cache (~{L3_matrix_dim}×{L3_matrix_dim})')

# Add text labels for cache boundaries
plt.text(L1d_matrix_dim*1.05, plt.ylim()[1]*0.95, f'L1d: {L1d_size_per_core:.1f}KB/core', rotation=90, fontsize=10)
plt.text(L2_matrix_dim*1.05, plt.ylim()[1]*0.95, f'L2: {L2_size_per_unit:.1f}MB/unit', rotation=90, fontsize=10)
plt.text(L3_matrix_dim*1.05, plt.ylim()[1]*0.95, f'L3: {L3_size_total}MB (shared)', rotation=90, fontsize=10)

# Mark best speedup point
plt.plot([best_size], [df_eng.loc[best_speedup_idx, 'naive_time']], 'r*', markersize=15)
plt.plot([best_size], [df_eng.loc[best_speedup_idx, 'optimized_time']], 'b*', markersize=15)
plt.annotate(f'Best Speedup: {best_speedup:.2f}x\n(n={best_size})',
             xy=(best_size, df_eng.loc[best_speedup_idx, 'naive_time']),
             xytext=(best_size*1.1, df_eng.loc[best_speedup_idx, 'naive_time']*1.1),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=12, bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8))

plt.title('Matrix-Vector Multiplication: Size vs. Execution Time', fontsize=16)
plt.xlabel('Matrix Dimension (n×n)', fontsize=14)
plt.ylabel('Execution Time (μs)', fontsize=14)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('matrix_execution_time.png', dpi=300)
plt.close()

# =========== Chart 2: Speedup Ratio ===========
plt.figure(figsize=(12, 7))

# Plot speedup curve
plt.plot(df_eng['size'], df_eng['speedup'], 'g-o', label='Speedup Ratio', linewidth=2.5, markersize=7)

# Add cache boundary lines
plt.axvline(x=L1d_matrix_dim, color='gray', linestyle='--', alpha=0.7, label=f'L1d Cache (~{L1d_matrix_dim}×{L1d_matrix_dim})')
plt.axvline(x=L2_matrix_dim, color='gray', linestyle=':', alpha=0.7, label=f'L2 Cache (~{L2_matrix_dim}×{L2_matrix_dim})')
plt.axvline(x=L3_matrix_dim, color='gray', linestyle='-.', alpha=0.7, label=f'L3 Cache (~{L3_matrix_dim}×{L3_matrix_dim})')

# Add text labels for cache boundaries
plt.text(L1d_matrix_dim*1.05, plt.ylim()[1]*0.95, f'L1d: {L1d_size_per_core:.1f}KB/core', rotation=90, fontsize=10)
plt.text(L2_matrix_dim*1.05, plt.ylim()[1]*0.95, f'L2: {L2_size_per_unit:.1f}MB/unit', rotation=90, fontsize=10)
plt.text(L3_matrix_dim*1.05, plt.ylim()[1]*0.95, f'L3: {L3_size_total}MB (shared)', rotation=90, fontsize=10)

# Mark best speedup point
plt.plot([best_size], [best_speedup], 'r*', markersize=15)
plt.annotate(f'Best Speedup: {best_speedup:.2f}x\n(n={best_size})',
             xy=(best_size, best_speedup),
             xytext=(best_size*1.1, best_speedup*0.9),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=12, bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8))

# Add baseline reference
plt.axhline(y=1.0, color='r', linestyle='-', alpha=0.5, label='No Speedup (1.0)')

# Add cache region annotations
plt.text(L1d_matrix_dim/2, plt.ylim()[1]*0.85, 'L1 Region', ha='center', fontsize=10, 
         bbox=dict(boxstyle="round", fc="white", alpha=0.8))
plt.text((L1d_matrix_dim+L2_matrix_dim)/2, plt.ylim()[1]*0.85, 'L2 Region', ha='center', fontsize=10, 
         bbox=dict(boxstyle="round", fc="white", alpha=0.8))
plt.text((L2_matrix_dim+L3_matrix_dim)/2, plt.ylim()[1]*0.85, 'L3 Region', ha='center', fontsize=10, 
         bbox=dict(boxstyle="round", fc="white", alpha=0.8))
plt.text((L3_matrix_dim+df_eng['size'].max())/2, plt.ylim()[1]*0.85, 'Memory Region', ha='center', fontsize=10, 
         bbox=dict(boxstyle="round", fc="white", alpha=0.8))

plt.title('Matrix-Vector Multiplication: Size vs. Speedup Ratio', fontsize=16)
plt.xlabel('Matrix Dimension (n×n)', fontsize=14)
plt.ylabel('Speedup Ratio (Naive/Optimized)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper left', fontsize=11)

plt.tight_layout()
plt.savefig('matrix_speedup.png', dpi=300)
plt.close()

print("Charts generated successfully!")