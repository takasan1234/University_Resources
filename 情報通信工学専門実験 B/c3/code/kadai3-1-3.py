import numpy as np
import matplotlib.pyplot as plt

# パラメータの設定
f = 2000  # 信号の周波数 2 kHz
A = np.sqrt(2)  # 振幅
fs1 = 10000  # サンプリング周波数 10 kHz
fs2 = 100000  # サンプリング周波数 100 kHz
N = 100000

# サンプリング時間
t1 = np.arange(0, 0.002, 1/fs1)  # 時間は0 msから2 ms (0.002秒)
t2 = np.arange(0, 0.002, 1/fs2)  # 高解像度用

# 正弦波データ生成
x1 = A * np.sin(2 * np.pi * f * t1)
x2 = A * np.sin(2 * np.pi * f * t2)  # 高解像度用

# フーリエ変換の実行
f_sin = np.fft.fft(x1)
f_index = np.fft.fftfreq(len(x1), 1/fs1)

# 振幅を正規化
f_sin_scaled = np.abs(f_sin) / len(x1)

# プロット
plt.figure()
plt.xlim([-4.5, 4.5])  # -5 kHz から 5 kHz まで表示
plt.stem(f_index[:N//2] / 1000, f_sin_scaled[:N//2], 'b', markerfmt=' ', basefmt="b")
plt.xlabel("Frequency [kHz]")
plt.ylabel("Absolute amplitude")
plt.legend(loc="upper right")
plt.grid()
plt.show()

