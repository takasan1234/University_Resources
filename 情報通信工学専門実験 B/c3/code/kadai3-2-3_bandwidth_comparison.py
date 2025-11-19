import numpy as np
import matplotlib.pyplot as plt

# パラメータの定義
fs = 10  # サンプリング周波数 [kHz]
data_size = int(1e5)  # サンプル数
tau = 100  # 矩形信号の時間幅 [ms]
T0 = 0  # 信号の中心

# 異なる帯域幅
W_values = [0.05, 0.1, 0.5]  # [kHz]
colors = ['red', 'blue', 'green']
labels = ['W=0.05 kHz', 'W=0.1 kHz', 'W=0.5 kHz']

# 時間軸の生成 (-5秒から5秒)
t = np.linspace(-5 * 1e3, 5 * 1e3, data_size)

# 矩形信号 r(t) の生成
r_t = np.where(np.abs(t - T0) <= tau / 2, 1, 0)

# フーリエ変換
f_rect = np.fft.fft(r_t)
f_index = np.fft.fftfreq(data_size, 1 / fs)

# 時間波形の比較プロット
plt.figure(figsize=(10, 6))
plt.plot(t, r_t, 'k--', linewidth=2, label='Original (Rectangular)', alpha=0.7)

for W, color, label in zip(W_values, colors, labels):
    # ローパスフィルタ H(f) の定義
    H_f = np.where(np.abs(f_index) <= W / 2, 1 + 0j, 0 + 0j)
    
    # フィルタ適用後のスペクトル
    filtered_spectrum = f_rect * H_f
    
    # 逆フーリエ変換
    filtered_signal = np.fft.ifft(filtered_spectrum).real
    
    plt.plot(t, filtered_signal, color=color, linewidth=1.5, label=label, alpha=0.8)

plt.xlim([-200, 200])
plt.ylim([-0.2, 1.2])
plt.xlabel("Time [ms]", fontsize=12)
plt.ylabel("Amplitude", fontsize=12)
plt.title("Comparison of LPF Output for Different Bandwidths", fontsize=14)
plt.legend(loc="upper right", fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../images/3-2-3_帯域比較_時間波形.png', dpi=150, bbox_inches='tight')
plt.show()

# スペクトルの比較プロット
plt.figure(figsize=(10, 6))

# 元の矩形信号のスペクトル
f_rect_shifted = np.fft.fftshift(f_rect)
f_index_shifted = np.fft.fftshift(f_index)
amplitude_spectrum_orig = np.abs(f_rect_shifted) / data_size
plt.plot(f_index_shifted, amplitude_spectrum_orig, 'k--', linewidth=2, 
         label='Original (Rectangular)', alpha=0.7)

for W, color, label in zip(W_values, colors, labels):
    # ローパスフィルタ H(f) の定義
    H_f = np.where(np.abs(f_index) <= W / 2, 1 + 0j, 0 + 0j)
    
    # フィルタ適用後のスペクトル
    filtered_spectrum = f_rect * H_f
    
    # 振幅絶対値スペクトル
    filtered_amplitude_spectrum = np.abs(np.fft.fftshift(filtered_spectrum)) / data_size
    
    plt.plot(f_index_shifted, filtered_amplitude_spectrum, 
             color=color, linewidth=1.5, label=label, alpha=0.8)

plt.xlim([-0.15, 0.15])
plt.ylim([0, np.max(amplitude_spectrum_orig) * 1.1])
plt.xlabel("Frequency [kHz]", fontsize=12)
plt.ylabel("Absolute amplitude", fontsize=12)
plt.title("Comparison of Amplitude Spectrum for Different Bandwidths", fontsize=14)
plt.legend(loc="upper right", fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../images/3-2-3_帯域比較_スペクトル.png', dpi=150, bbox_inches='tight')
plt.show()

print("図の生成が完了しました。")
print("- 3-2-3_帯域比較_時間波形.png")
print("- 3-2-3_帯域比較_スペクトル.png")


