import matplotlib.pyplot as plt
import numpy as np
from scipy.special import jv  # ベッセル関数
import matplotlib

# 日本語フォントの設定
matplotlib.rcParams['font.family'] = 'Hiragino Sans'
matplotlib.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Hiragino Kaku Gothic Pro']
matplotlib.rcParams['axes.unicode_minus'] = False

# 観測データ
A_s = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])  # V

# 各成分のピーク値 (mV)
carrier = np.array([268.2, 210.5, 142.0, 65.09, 12.95, 75.42])      # 搬送波成分 (1MHz)
fundamental = np.array([59.11, 112.8, 148.3, 148.2, 146.4, 92.92])  # 基本波成分 (1.1MHz)
second_harmonic = np.array([8.957, 34.43, 68.94, 102.4, 112.2, 145.9])  # 2次高調波成分 (1.2MHz)

# ベッセル関数のフィッティング用の連続データ
A_s_fit = np.linspace(0, 3.5, 200)

# スケーリング係数を推定（最大値に合わせる）
scale_J0 = np.max(carrier)
scale_J1 = np.max(fundamental)
scale_J2 = np.max(second_harmonic)

# ベッセル関数を計算（引数を調整）
# 変調度 k_p は A_s に比例すると仮定し、調整係数を掛ける
k_factor = 1.5  # この係数で調整
J0_fit = scale_J0 * np.abs(jv(0, k_factor * A_s_fit))
J1_fit = scale_J1 * np.abs(jv(1, k_factor * A_s_fit))
J2_fit = scale_J2 * np.abs(jv(2, k_factor * A_s_fit))

# グラフの作成
plt.figure(figsize=(12, 8))

# 搬送波成分
plt.plot(A_s, carrier, 'o', markersize=8, color='blue', label='搬送波成分 (1MHz) 観測値')
plt.plot(A_s_fit, J0_fit, '-', linewidth=2, color='blue', alpha=0.7, label='$|J_0(x)|$ フィッティング')

# 基本波成分
plt.plot(A_s, fundamental, 's', markersize=8, color='red', label='基本波成分 (1.1MHz) 観測値')
plt.plot(A_s_fit, J1_fit, '-', linewidth=2, color='red', alpha=0.7, label='$|J_1(x)|$ フィッティング')

# 2次高調波成分
plt.plot(A_s, second_harmonic, '^', markersize=8, color='green', label='2次高調波成分 (1.2MHz) 観測値')
plt.plot(A_s_fit, J2_fit, '-', linewidth=2, color='green', alpha=0.7, label='$|J_2(x)|$ フィッティング')

# グラフの設定
plt.xlabel('変調信号の振幅 $A_s$ [V]', fontsize=14)
plt.ylabel('ピーク値 [mV]', fontsize=14)
plt.title('正弦波位相変調における各成分のピーク値の$A_s$依存性とベッセル関数フィッティング', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11, loc='upper right')
plt.xlim(0, 3.5)
plt.ylim(0, 300)

# グラフを保存
plt.tight_layout()
plt.savefig('pm_bessel_fitting.png', dpi=300, bbox_inches='tight')
print(f"グラフを保存しました: pm_bessel_fitting.png")

