import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.font_manager as fm
import glob
import os

# MacOSの日本語フォントを設定
plt.rcParams['font.family'] = 'Hiragino Sans GB'
plt.rcParams['axes.unicode_minus'] = False

# コマンドライン引数でCSVファイルを指定できるようにする
input_file = "results_simple.csv"  # デフォルトのファイル名
output_prefix = "blocking_rate"      # デフォルトの出力ファイル名
compare_lambdas = False              # λ値を比較するかどうか

if len(sys.argv) > 1:
    if sys.argv[1] == "compare_lambdas":
        compare_lambdas = True
        output_prefix = "comparison_all_lambdas"
    else:
        input_file = sys.argv[1]
        # 出力ファイル名をCSVファイル名に基づいて変更
        output_prefix = "graph_" + input_file.replace(".csv", "")

# λ値の比較グラフを生成
if compare_lambdas:
    # 各経路選択方法ごとにλ値を比較するグラフを作成
    route_methods = [
        "min_hop_fixed", 
        "max_path_fixed", 
        "min_hop_demand", 
        "max_path_demand", 
        "inverse_capacity", 
        "shortest_widest"
    ]
    
    route_labels = [
        "Min Hop Route (Fixed)", 
        "Max Path (Fixed)", 
        "Min Hop Route (On Demand)", 
        "Max Path (On Demand)", 
        "Route Considering Inverse Capacity", 
        "Shortest Widest Path"
    ]
    
    # 各経路選択方法ごとに別々のグラフを作成
    for method_idx, method in enumerate(route_methods):
        plt.figure(figsize=(12, 8))
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xlabel('Parameter n', fontsize=14)
        plt.ylabel('Blocking Rate', fontsize=14)
        plt.title(f'Effect of λ on Blocking Rate: {route_labels[method_idx]}', fontsize=16)
        
        # 用意する色のリスト
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']
        
        # すべてのλ値のCSVファイルを取得
        csv_files = sorted(glob.glob("results_exponential_lambda_*.csv"))
        
        # 各ファイルから対応する列のデータを抽出してプロット
        for i, csv_file in enumerate(csv_files):
            try:
                df = pd.read_csv(csv_file)
                param_n = df['n'].tolist()
                data = df[method].tolist()
                
                # ファイル名からλ値を抽出
                lambda_str = os.path.basename(csv_file).replace("results_exponential_lambda_", "").replace(".csv", "")
                lambda_val = float(lambda_str.replace("_", "."))
                
                # λ値ごとに異なる色でプロット
                plt.plot(param_n, data, 'o-', 
                        label=f'λ = {lambda_val:.5f}', 
                        linewidth=2, 
                        color=colors[i % len(colors)])
            except Exception as e:
                print(f"Error reading {csv_file}: {str(e)}")
        
        # Legend settings
        plt.legend(loc='best', fontsize=12)
        
        # x-axis ticks
        plt.xticks(param_n)
        
        # y-axis range
        plt.ylim(0, 1.0)
        
        # 各方式ごとのグラフを保存
        method_output = f'{output_prefix}_{method}'
        plt.savefig(f'{method_output}.pdf')
        plt.savefig(f'{method_output}.png')
        print(f"Comparison graph created for {method}. {method_output}.pdf and {method_output}.png have been saved.")
    
    # すべての方式を比較した総合グラフも作成
    plt.figure(figsize=(15, 10))
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel('Parameter n', fontsize=14)
    plt.ylabel('Blocking Rate', fontsize=14)
    plt.title(f'Comparison of All Routing Methods and λ Values', fontsize=16)
    
    # λ値とルーティング方式の組み合わせをプロット
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D', '*', 'X', 'P', 'p', 'h']
    
    for i, csv_file in enumerate(csv_files):
        try:
            df = pd.read_csv(csv_file)
            param_n = df['n'].tolist()
            
            # ファイル名からλ値を抽出
            lambda_str = os.path.basename(csv_file).replace("results_exponential_lambda_", "").replace(".csv", "")
            lambda_val = float(lambda_str.replace("_", "."))
            
            for j, method in enumerate(route_methods):
                data = df[method].tolist()
                plt.plot(param_n, data, 
                        marker=markers[j % len(markers)], 
                        linestyle=linestyles[i % len(linestyles)],
                        label=f'{route_labels[j]} (λ={lambda_val:.5f})', 
                        linewidth=1.5)
        except Exception as e:
            print(f"Error reading {csv_file}: {str(e)}")
    
    # Legend settings for the combined graph
    plt.legend(loc='best', fontsize=10)
    plt.xticks(param_n)
    plt.ylim(0, 1.0)
    
    # 総合グラフを保存
    plt.savefig(f'{output_prefix}_combined.pdf')
    print(f"Combined comparison graph created. {output_prefix}_combined.pdf and {output_prefix}_combined.png have been saved.")
    
    # 終了
    sys.exit(0)

# 通常の単一ファイルグラフ作成処理
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