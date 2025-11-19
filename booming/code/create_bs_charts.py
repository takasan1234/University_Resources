import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import csv
import re

# 日本語フォントの設定
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# CSVファイルの読み込み
def parse_number(value):
    """数値文字列を数値に変換（カンマを除去）"""
    if isinstance(value, (int, float)):
        if np.isnan(value):
            return 0.0
        return float(value)
    if isinstance(value, str):
        # カンマを除去
        cleaned = value.replace(',', '').replace('"', '').strip()
        if cleaned == '' or cleaned.lower() == 'nan':
            return 0.0
        try:
            return float(cleaned)
        except:
            return 0.0
    return 0.0

# CSVファイルを読み込む
data = []
with open('../data/入力_5社.csv', 'r', encoding='utf-8-sig') as f:  # utf-8-sigでBOMを除去
    reader = csv.reader(f, quotechar='"', skipinitialspace=True)
    header = next(reader)
    # 列名の前後の空白を削除
    header = [col.strip() for col in header]
    
    for row in reader:
        if len(row) > 0 and row[0].strip():  # 空行をスキップ
            # 各セルの前後の空白を削除
            row = [cell.strip() for cell in row]
            data.append(row)

# 列名のインデックスを取得
company_idx = header.index('会社名')
current_assets_idx = header.index('流動資産')
fixed_assets_idx = header.index('固定資産')
current_liabilities_idx = header.index('流動負債')
fixed_liabilities_idx = header.index('固定負債')
equity_idx = header.index('自己資本（純資産）')

# 各社のBSグラフを作成
for row in data:
    if len(row) <= company_idx:
        continue
    
    company = row[company_idx].strip()
    if not company or company == '':
        continue
    
    # データの取得
    current_assets = parse_number(row[current_assets_idx] if len(row) > current_assets_idx else '0')
    fixed_assets = parse_number(row[fixed_assets_idx] if len(row) > fixed_assets_idx else '0')
    current_liabilities = parse_number(row[current_liabilities_idx] if len(row) > current_liabilities_idx else '0')
    fixed_liabilities = parse_number(row[fixed_liabilities_idx] if len(row) > fixed_liabilities_idx else '0')
    equity = parse_number(row[equity_idx] if len(row) > equity_idx else '0')
    
    # 総資産と総負債・純資産の計算（BSのバランス確認）
    total_assets = current_assets + fixed_assets
    total_liabilities_equity = current_liabilities + fixed_liabilities + equity
    
    print(f'{company}: 総資産={total_assets:,.0f}, 負債+純資産={total_liabilities_equity:,.0f}')
    
    # グラフの作成（積み上げ棒グラフで左右対称に表示）
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # X軸の位置（左：資産の部、右：負債・純資産の部）
    x_positions = [0, 1]
    x_labels = ['資産の部', '負債・純資産の部']
    width = 0.6
    
    # 資産の部の積み上げ（下から上へ：流動資産、固定資産）
    asset_bottom = [0]
    asset_values = [current_assets, fixed_assets]
    asset_colors = ['#4A90E2', '#7B68EE']
    asset_labels = ['流動資産', '固定資産']
    
    bars_assets = []
    for i, (value, color, label) in enumerate(zip(asset_values, asset_colors, asset_labels)):
        bar = ax.bar(x_positions[0], value, width, bottom=asset_bottom[0], 
                    color=color, alpha=0.8, label=label)
        bars_assets.append(bar)
        # 数値を表示
        if value > 0:
            ax.text(x_positions[0], asset_bottom[0] + value/2, 
                   f'{label}\n{value:,.0f}',
                   ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        asset_bottom[0] += value
    
    # 負債・純資産の部の積み上げ（下から上へ：流動負債、固定負債、純資産）
    liability_bottom = [0]
    liability_values = [current_liabilities, fixed_liabilities, equity]
    liability_colors = ['#E74C3C', '#F39C12', '#27AE60']
    liability_labels = ['流動負債', '固定負債', '純資産']
    
    bars_liabilities = []
    for i, (value, color, label) in enumerate(zip(liability_values, liability_colors, liability_labels)):
        bar = ax.bar(x_positions[1], value, width, bottom=liability_bottom[0], 
                    color=color, alpha=0.8, label=label)
        bars_liabilities.append(bar)
        # 数値を表示
        if value > 0:
            ax.text(x_positions[1], liability_bottom[0] + value/2, 
                   f'{label}\n{value:,.0f}',
                   ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        liability_bottom[0] += value
    
    # グラフの装飾
    ax.set_ylabel('金額 (百万円)', fontsize=12, fontweight='bold')
    ax.set_title(f'{company} 貸借対照表', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Y軸のスケールを統一（両方の合計が同じ高さになるように）
    max_height = max(total_assets, total_liabilities_equity)
    ax.set_ylim(0, max_height * 1.1)
    
    # 合計値を表示
    ax.text(x_positions[0], total_assets, f'合計: {total_assets:,.0f}',
           ha='center', va='bottom', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax.text(x_positions[1], total_liabilities_equity, f'合計: {total_liabilities_equity:,.0f}',
           ha='center', va='bottom', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    
    # 凡例を表示（重複を避ける）
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=9, framealpha=0.9)
    
    # レイアウトの調整
    plt.tight_layout()
    
    # ファイル名の安全化（スラッシュなどを除去）
    safe_company_name = company.replace('/', '_').replace('\\', '_')
    output_path = f'../assets/BS/bs_{safe_company_name}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f'グラフを保存しました: {output_path}')
    
    plt.close()

print('すべてのBSグラフの生成が完了しました！')

