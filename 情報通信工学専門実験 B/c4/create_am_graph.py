import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 日本語フォントの設定
matplotlib.rcParams['font.family'] = 'Hiragino Sans'
matplotlib.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Hiragino Kaku Gothic Pro']
matplotlib.rcParams['axes.unicode_minus'] = False

# データ
A_m = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])  # V
peak_values = np.array([148.3, 311.3, 462.4, 573.6, 689.3, 988.6])  # mV

# 一次近似
coeffs = np.polyfit(A_m, peak_values, 1)
a = coeffs[0]  # 傾き
b = coeffs[1]  # 切片

# 近似直線
A_m_line = np.linspace(0, 3.5, 100)
peak_line = a * A_m_line + b

# グラフの作成
plt.figure(figsize=(10, 7))

# 観測値のプロット
plt.plot(A_m, peak_values, 'o', markersize=8, color='blue', label='観測値')

# 一次近似直線のプロット
plt.plot(A_m_line, peak_line, '-', linewidth=2, color='red', 
         label=f'一次近似直線: y = {a:.2f}x + {b:.2f}')

# グラフの設定
plt.xlabel('変調信号の振幅 $A_m$ [V]', fontsize=14)
plt.ylabel('ピーク値 [mV]', fontsize=14)
plt.title('ピーク値の$A_m$依存性（1.1 MHzにおけるピーク値）', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.xlim(0, 3.5)
plt.ylim(0, 1100)

# グラフを保存
plt.tight_layout()
plt.savefig('am_peak_dependency.png', dpi=300, bbox_inches='tight')
print(f"グラフを保存しました: am_peak_dependency.png")
print(f"一次近似式: y = {a:.2f}x + {b:.2f}")
print(f"相関係数: {np.corrcoef(A_m, peak_values)[0, 1]:.4f}")

