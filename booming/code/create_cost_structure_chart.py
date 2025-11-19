import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 日本語フォントの設定
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# データの準備
companies = ['ユナイテッドアローズ\n(UA)', 'ワークマン', 'しまむら', 'アダストリア', 'FR\n(ファーストリテイリング)']
cogs = [47.9, 62.6, 65.3, 45.3, 46.1]  # 原価 (COGS)
p_cost = [14.5, 3.1, 11.1, None, 14.1]  # 人件費 (P-Cost)
other_sga = [32.4, 16.4, 14.9, None, 24.2]  # その他販管費 (Other SG&A)
op = [5.3, 17.8, 8.9, 5.3, 16.1]  # 営業利益 (OP)

# Noneを0に変換（グラフ表示用）
cogs_plot = [x if x is not None else 0 for x in cogs]
p_cost_plot = [x if x is not None else 0 for x in p_cost]
other_sga_plot = [x if x is not None else 0 for x in other_sga]
op_plot = [x if x is not None else 0 for x in op]

# グラフの作成
fig, ax = plt.subplots(figsize=(12, 7))

# 積み上げ棒グラフの位置
x = np.arange(len(companies))
width = 0.6

# 各項目を積み上げ
bottom1 = np.array(cogs_plot)
bottom2 = bottom1 + np.array(p_cost_plot)
bottom3 = bottom2 + np.array(other_sga_plot)

# バーの描画
bars1 = ax.bar(x, cogs_plot, width, label='原価 (COGS)', color='#FF6B6B', alpha=0.8)
bars2 = ax.bar(x, p_cost_plot, width, bottom=bottom1, label='人件費 (P-Cost)', color='#4ECDC4', alpha=0.8)
bars3 = ax.bar(x, other_sga_plot, width, bottom=bottom2, label='その他販管費 (Other SG&A)', color='#95E1D3', alpha=0.8)
bars4 = ax.bar(x, op_plot, width, bottom=bottom3, label='営業利益 (OP)', color='#F38181', alpha=0.8)

# グラフの装飾
ax.set_ylabel('売上高に対する割合 (%)', fontsize=12, fontweight='bold')
ax.set_title('各社の費用構成比較', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(companies, fontsize=10)
ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
ax.set_ylim(0, 105)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# 各バーに数値を表示（N/Aの場合は表示しない）
for i, (c, p, o, op_val) in enumerate(zip(cogs, p_cost, other_sga, op)):
    y_pos = 0
    if c is not None:
        ax.text(i, y_pos + c/2, f'{c:.1f}%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        y_pos += c
    if p is not None:
        ax.text(i, y_pos + p/2, f'{p:.1f}%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        y_pos += p
    if o is not None:
        ax.text(i, y_pos + o/2, f'{o:.1f}%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        y_pos += o
    if op_val is not None:
        ax.text(i, y_pos + op_val/2, f'{op_val:.1f}%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# レイアウトの調整
plt.tight_layout()

# 保存
output_path = '../assets/cost_structure/cost_structure_comparison.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'グラフを保存しました: {output_path}')

plt.close()

