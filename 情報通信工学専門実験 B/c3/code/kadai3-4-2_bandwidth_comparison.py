import numpy as np
import matplotlib.pyplot as plt

# パラメータの定義
fs = np.float64(10)  # サンプリング周波数 [kHz]
data_size = np.int64(1e5)  # サンプル数

rect_width = np.float64(100)  # 矩形信号の時間幅 [msec]
T0 = data_size * 1 / fs / 2

# 異なる帯域幅
W_values = [0.05, 0.1, 0.5]  # [kHz]
colors = ['red', 'blue', 'green']
labels = ['W=0.05 kHz', 'W=0.1 kHz', 'W=0.5 kHz']

n_var = np.float64(1)  # 白色ガウス雑音の分散

# 時間軸の生成
t_index = np.arange(data_size) * 1 / fs
t_rect = np.float64(np.abs(t_index - T0) <= rect_width / 2)
t_noise = np.random.normal(0.0, np.sqrt(n_var), data_size)

t_rect_noise = t_rect + t_noise

# 周波数軸の生成とフーリエ変換
f_index = np.fft.fftfreq(data_size, 1 / fs)
f_rect_noise = np.fft.fft(t_rect_noise)
f_rect = np.fft.fft(t_rect)

# 時間波形の比較プロット
plt.figure(figsize=(10, 6))
plt.plot(t_index - T0, t_rect, 'k--', linewidth=2, label='Original (Rect)', alpha=0.7)
plt.plot(t_index - T0, t_rect_noise, color='gray', linewidth=0.5, 
         label='Rect + Noise', alpha=0.5)

for W, color, label in zip(W_values, colors, labels):
    # ローパスフィルタ
    f_LPF = np.complex128(np.abs(f_index) <= W / 2)
    f_rect_LPF = f_LPF * f_rect_noise
    t_rect_LPF = np.fft.ifft(f_rect_LPF).real
    
    plt.plot(t_index - T0, t_rect_LPF, color=color, linewidth=1.5, 
             label=f'Filtered ({label})', alpha=0.8)

plt.xlim([-200, 200])
plt.ylim([-0.5, 1.5])
plt.xlabel("Time [ms]", fontsize=12)
plt.ylabel("Amplitude", fontsize=12)
plt.title("Noise Suppression vs. Signal Distortion for Different Bandwidths", fontsize=14)
plt.legend(loc="upper right", fontsize=9)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../images/3-4-2_帯域比較_時間波形.png', dpi=150, bbox_inches='tight')
plt.show()

# スペクトルの比較プロット
plt.figure(figsize=(10, 6))

# 元の矩形信号のスペクトル
plt.plot(np.fft.fftshift(f_index), np.fft.fftshift(np.abs(f_rect))/data_size, 
         'k--', linewidth=2, label='Original (Rect)', alpha=0.7)
plt.plot(np.fft.fftshift(f_index), np.fft.fftshift(np.abs(f_rect_noise))/data_size, 
         color='gray', linewidth=0.5, label='Rect + Noise', alpha=0.5)

for W, color, label in zip(W_values, colors, labels):
    # ローパスフィルタ
    f_LPF = np.complex128(np.abs(f_index) <= W / 2)
    f_rect_LPF = f_LPF * f_rect_noise
    
    plt.plot(np.fft.fftshift(f_index), np.fft.fftshift(np.abs(f_rect_LPF))/data_size, 
             color=color, linewidth=1.5, label=f'Filtered ({label})', alpha=0.8)

plt.xlim([-0.15, 0.15])
plt.ylim([0, 0.015])
plt.xlabel("Frequency [kHz]", fontsize=12)
plt.ylabel("Absolute Amplitude", fontsize=12)
plt.title("Spectrum Comparison for Different Bandwidths", fontsize=14)
plt.legend(loc="upper right", fontsize=9)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../images/3-4-2_帯域比較_スペクトル.png', dpi=150, bbox_inches='tight')
plt.show()

print("図の生成が完了しました。")
print("- 3-4-2_帯域比較_時間波形.png")
print("- 3-4-2_帯域比較_スペクトル.png")


