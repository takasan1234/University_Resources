import numpy as np
import matplotlib.pyplot as plt

# パラメータの定義
fs = 10  # サンプリング周波数 [kHz]
data_size = int(1e5)  # サンプル数
tau = 100  # 矩形信号の時間幅 [ms]
T0 = 0  # 信号の中心
W = 0.1  # ローパスフィルタの帯域 [kHz]

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

# ローパスフィルタ H(f) の定義
H_f = np.where(np.abs(f_index) <= W / 2, 1 + 0j, 0 + 0j)

# フィルタ適用後のスペクトル R(f) * H(f)
filtered_spectrum = f_rect * H_f

# フィルタ適用後の信号を逆フーリエ変換
filtered_signal = np.fft.ifft(filtered_spectrum).real

# 振幅絶対値スペクトル（フィルタ後）の計算
filtered_amplitude_spectrum = np.abs(np.fft.fftshift(filtered_spectrum)) / data_size

# 図のプロット

# フィルタ出力の時間波形のプロット
plt.figure(figsize=(6, 4))
plt.plot(t, filtered_signal, label="Filtered Signal")
plt.xlim([-200, 200])
plt.ylim([-0.2, 1.2])
plt.xlabel("Time [ms]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

# フィルタ後の振幅スペクトルのプロット
plt.figure(figsize=(6, 4))
plt.plot(f_index_shifted, filtered_amplitude_spectrum, label="Filtered Amplitude Spectrum")
plt.xlim([-0.1, 0.1])  # 周波数軸の範囲を設定
plt.ylim([0, np.max(filtered_amplitude_spectrum) * 1.1])  # 振幅スペクトルの範囲を自動調整
plt.xlabel("Frequency [kHz]")
plt.ylabel("Absolute amplitude")
plt.grid(True)
plt.show()
