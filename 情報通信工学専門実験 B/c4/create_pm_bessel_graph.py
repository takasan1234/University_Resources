import matplotlib.pyplot as plt
import numpy as np
from scipy.special import jv  # ベッセル関数
from scipy.optimize import curve_fit
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

# ベッセル関数のフィッティング関数を定義
def bessel_J0(x, scale, k):
    return scale * np.abs(jv(0, k * x))

def bessel_J1(x, scale, k):
    return scale * np.abs(jv(1, k * x))

def bessel_J2(x, scale, k):
    return scale * np.abs(jv(2, k * x))

# 各成分に対してフィッティングを実行
# 初期推定値: scale は最大値、k は 1.0 程度
try:
    popt_J0, _ = curve_fit(bessel_J0, A_s, carrier, p0=[300, 1.0], maxfev=5000)
    popt_J1, _ = curve_fit(bessel_J1, A_s, fundamental, p0=[150, 1.0], maxfev=5000)
    popt_J2, _ = curve_fit(bessel_J2, A_s, second_harmonic, p0=[150, 1.0], maxfev=5000)
    
    print(f"J0 フィッティングパラメータ: scale={popt_J0[0]:.2f}, k={popt_J0[1]:.3f}")
    print(f"J1 フィッティングパラメータ: scale={popt_J1[0]:.2f}, k={popt_J1[1]:.3f}")
    print(f"J2 フィッティングパラメータ: scale={popt_J2[0]:.2f}, k={popt_J2[1]:.3f}")
except Exception as e:
    print(f"フィッティングエラー: {e}")
    # フォールバック
    popt_J0 = [280, 1.3]
    popt_J1 = [150, 1.3]
    popt_J2 = [150, 1.3]

# ベッセル関数のフィッティング用の連続データ
A_s_fit = np.linspace(0, 3.5, 200)

# フィッティング結果を使って曲線を生成
J0_fit = bessel_J0(A_s_fit, *popt_J0)
J1_fit = bessel_J1(A_s_fit, *popt_J1)
J2_fit = bessel_J2(A_s_fit, *popt_J2)

# グラフの作成
plt.figure(figsize=(12, 8))

# 搬送波成分
plt.plot(A_s, carrier, 'o', markersize=8, color='blue', label='搬送波成分 (1MHz) 観測値')
plt.plot(A_s_fit, J0_fit, '-', linewidth=2, color='blue', alpha=0.7, 
         label=f'$|J_0({popt_J0[1]:.2f}x)|$ フィッティング')

# 基本波成分
plt.plot(A_s, fundamental, 's', markersize=8, color='red', label='基本波成分 (1.1MHz) 観測値')
plt.plot(A_s_fit, J1_fit, '-', linewidth=2, color='red', alpha=0.7, 
         label=f'$|J_1({popt_J1[1]:.2f}x)|$ フィッティング')

# 2次高調波成分
plt.plot(A_s, second_harmonic, '^', markersize=8, color='green', label='2次高調波成分 (1.2MHz) 観測値')
plt.plot(A_s_fit, J2_fit, '-', linewidth=2, color='green', alpha=0.7, 
         label=f'$|J_2({popt_J2[1]:.2f}x)|$ フィッティング')

# グラフの設定
plt.xlabel('変調信号の振幅 $A_m$ [V]', fontsize=14)
plt.ylabel('ピーク値 [mV]', fontsize=14)
plt.title('正弦波位相変調における各成分のピーク値の$A_m$依存性とベッセル関数フィッティング', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11, loc='upper right')
plt.xlim(0, 3.5)
plt.ylim(0, 300)

# グラフを保存
plt.tight_layout()
plt.savefig('pm_bessel_fitting.png', dpi=300, bbox_inches='tight')
print(f"グラフを保存しました: pm_bessel_fitting.png")

