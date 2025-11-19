import numpy as np
import matplotlib.pyplot as plt

A = np.sqrt(2)  # 振幅
f = 2000  # 周波数 2 kHz
fs1 = 10000  # サンプリング周波数 10 kHz
fs2 = 100000  # サンプリング周波数 100 kHz
N = 100000 # サンプル数

# サンプリング時間
t1 = np.arange(0, 0.002, 1/fs1)  # 時間は0 msから2 ms (0.002秒)
t2 = np.arange(0, 0.002, 1/fs2)  # 高解像度用

# 正弦波データ生成
x1 = A * np.sin(2 * np.pi * f * t1)
x2 = A * np.sin(2 * np.pi * f * t2)  # 高解像度用

plt.figure()
plt.xlim([0, 2])  # 時間軸はミリ秒 (0ms - 2ms)
plt.ylim([-1.5, 1.5])  # 振幅範囲
plt.plot(t1 * 1000, x1, 'bo', label="Samples(sfreq = 10 kHz)")  # サンプリングデータ (10 kHz)
plt.plot(t2 * 1000, x2, '--', label="Sine curve(sfreq = 100 kHz)")  # 高解像度波形 (100 kHz)
plt.xlabel("Time [ms]")
plt.ylabel("Amplitude")
plt.legend(loc="upper right")
plt.grid()
plt.show()

