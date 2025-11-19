import numpy as np
import matplotlib.pyplot as plt

# パラメータの定義
fs = np.float64(10)  # サンプリング周波数 [kHz]
data_size = np.int64(1e5)  # サンプル数

rect_width = np.float64(100)  # 矩形信号の時間幅 [msec]
T0 = data_size * 1 / fs / 2

# フィルタの帯域幅
LPF_width = np.float64(0.1)  # kHz

n_var = np.float64(1)  # 白色ガウス雑音の分散

# 時間軸の生成
t_index = np.arange(data_size) * 1 / fs
t_rect = np.float64(np.abs(t_index - T0) <= rect_width / 2)
t_noise = np.random.normal(0.0, np.sqrt(n_var), data_size)

t_rect_noise = t_rect + t_noise

# 周波数軸の生成とフーリエ変換
f_index = np.fft.fftfreq(data_size, 1 / fs)
f_rect_noise = np.fft.fft(t_rect_noise)

# ローパスフィルタ
f_LPF = np.complex128(np.abs(f_index) <= LPF_width / 2)
f_rect_LPF = f_LPF * f_rect_noise
t_rect_LPF = np.fft.ifft(f_rect_LPF).real

# 矩形信号のフーリエ変換
f_rect = np.fft.fft(t_rect)

# 図のプロット (時間波形)
plt.figure(figsize=(7, 5))
plt.plot(t_index - T0, t_rect_noise, label="Rect + noise", color='blue', alpha=0.7)
plt.plot(t_index - T0, t_rect_LPF, label="Filtered", color='orange')
plt.plot(t_index - T0, t_rect, label="Rect", color='green', linestyle='--')
plt.xlim([-200, 200])  # 時間軸を -200 から 200 msに設定
plt.ylim([-0.5, 1.50])
plt.xlabel("Time [ms]")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

# 図のプロット (周波数スペクトル)
plt.figure(figsize=(7, 5))
plt.plot(np.fft.fftshift(f_index), np.fft.fftshift(np.abs(f_rect_noise))/100000, label="Rect + noise", color='blue', alpha=0.7)
plt.plot(np.fft.fftshift(f_index), np.fft.fftshift(np.abs(f_rect_LPF))/100000, label="Filtered", color='orange')
plt.plot(np.fft.fftshift(f_index), np.fft.fftshift(np.abs(f_rect))/100000, label="Rect", color='green', linestyle='--')
plt.xlim([-0.1, 0.1])
plt.ylim([0, 0.015])
plt.xlabel("Frequency [kHz]")
plt.ylabel("Absolute Amplitude")
plt.legend()
plt.show()
