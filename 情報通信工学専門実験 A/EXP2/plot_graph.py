import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.font_manager as fm

# MacOSの日本語フォントを設定
plt.rcParams['font.family'] = 'Hiragino Sans GB'
plt.rcParams['axes.unicode_minus'] = False

# コマンドライン引数でCSVファイルを指定できるようにする
input_file = "results_simple.csv"  # デフォルトのファイル名
output_prefix = "blocking_rate"      # デフォルトの出力ファイル名

if len(sys.argv) > 1:
    input_file = sys.argv[1]
    # 出力ファイル名をCSVファイル名に基づいて変更
    output_prefix = "graph_" + input_file.replace(".csv", "")

# Read data from CSV file
try:
    # Read CSV file using pandas
    df = pd.read_csv(input_file)
    
    # Extract data from DataFrame
    param_n = df['n'].tolist()
    min_hop_fixed = df['min_hop_fixed'].tolist()
    max_path_fixed = df['max_path_fixed'].tolist()
    min_hop_demand = df['min_hop_demand'].tolist()
    max_path_demand = df['max_path_demand'].tolist()
    inverse_capacity = df['inverse_capacity'].tolist()
    shortest_widest = df['shortest_widest'].tolist()
except FileNotFoundError:
    print(f"Error: {input_file} not found. Please run simulation first.")
    exit(1)
except Exception as e:
    print(f"Error reading {input_file}: {str(e)}")
    exit(1)

# Create figure
plt.figure(figsize=(12, 8))

# Graph style
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel('Parameter n', fontsize=14)
plt.ylabel('Blocking Rate', fontsize=14)
plt.title(f'Relationship between Parameter n and Blocking Rate ({input_file})', fontsize=16)

# Plot different routing methods
plt.plot(param_n, min_hop_fixed, 'o-', label='Min Hop Route (Fixed)', linewidth=2)
plt.plot(param_n, max_path_fixed, 's-', label='Max Path (Fixed)', linewidth=2)
plt.plot(param_n, min_hop_demand, '^-', label='Min Hop Route (On Demand)', linewidth=2)
plt.plot(param_n, max_path_demand, 'D-', label='Max Path (On Demand)', linewidth=2)
plt.plot(param_n, inverse_capacity, '*-', label='Route Considering Inverse Capacity', linewidth=2)
plt.plot(param_n, shortest_widest, 'X-', label='Shortest Widest Path', linewidth=2)

# Legend settings
plt.legend(loc='best', fontsize=12)

# x-axis ticks
plt.xticks(param_n)

# y-axis range
plt.ylim(0, 1.0)

# Save
plt.savefig(f'{output_prefix}.pdf')
plt.savefig(f'{output_prefix}.png')

print(f"Graph created. {output_prefix}.pdf and {output_prefix}.png have been saved.") 