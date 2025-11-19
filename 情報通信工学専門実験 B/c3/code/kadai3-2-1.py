import numpy as np
import matplotlib.pyplot as plt

# パラメータの定義
fs = 10  # サンプリング周波数 [kHz]
data_size = int(1e5)  # サンプル数
tau = 100  # 矩形信号の時間幅 [ms]
T0 = 0  # 信号の中心

# 時間軸の生成 (-5秒から5秒)
t = np.linspace(-5 * 1e3, 5 * 1e3, data_size)

# 矩形信号 r(t) の生成
r_t = np.where(np.abs(t - T0) <= tau / 2, 1, 0)

# フーリエ変換
f_rect = np.fft.fft(r_t)
f_index = np.fft.fftfreq(data_size, 1 / fs)  # 周波数軸の生成
f_rect_shifted = np.fft.fftshift(f_rect)  # FFT結果をシフト
f_index_shifted = np.fft.fftshift(f_index)  # 周波数軸もシフト

# 振幅絶対値スペクトルの計算
amplitude_spectrum = np.abs(f_rect_shifted) / data_size

# 時間領域の矩形信号のプロット
plt.figure(figsize=(6, 4))
plt.plot(t, r_t, label="Rectangular Signal")
plt.xlim([-200, 200])
plt.ylim([-0.2, 1.2])
plt.xlabel("Time [ms]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

# フーリエ変換の振幅スペクトルをプロット
plt.figure(figsize=(6, 4))
plt.plot(f_index_shifted, amplitude_spectrum, label="Amplitude Spectrum")
plt.xlim([-0.1, 0.1])  # 周波数軸の範囲を設定
plt.ylim([0, np.max(amplitude_spectrum) * 1.1])  # 振幅スペクトルの範囲を自動調整
plt.xlabel("Frequency [kHz]")
plt.ylabel("Absolute amplitude")
plt.grid(True)
plt.show()
