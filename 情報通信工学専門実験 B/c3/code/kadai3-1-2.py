import numpy as np
import matplotlib.pyplot as plt

A = np.sqrt(2)  # 振幅
f = 2000  # 周波数 2 kHz
fs1 = 10000  # サンプリング周波数 10 kHz
fs2 = 100000  # サンプリング周波数 100 kHz
N = 100000 # サンプル数

# サンプリング時間
t1 = np.arange(N)/fs1 # 時間は0 msから2 ms (0.002秒)
t2 = np.arange(N)/fs2 #高解像度用

# 正弦波データ生成
x1 = A * np.sin(2 * np.pi * f * t1)
x2 = A * np.sin(2 * np.pi * f * t2)  # 高解像度用

t_intencity = x1**2 # 時間領域の強度
dt = 1/fs1
t_energy = np.sum(t_intencity * dt)

T = N * dt #何秒間サンプルを得たか
power = t_energy / T # パワーは単位時間あたりのエネルギー

average_intencity = np.mean(t_intencity)

# 時間領域での信号 x1 をフーリエ変換し、周波数領域での強度、エネルギー、パワーを計算
f_sin = np.fft.fft(x1)
f_index = np.fft.fftfreq(N, 1/fs1)
f_intensity = np.abs(f_sin)*np.abs(f_sin)
f_energy = (f_intensity).sum()
f_power = f_energy/N



print(f"エネルギー(時間領域):{t_energy}")
print(f"パワー(時間領域):{power}")
print(f"平均強度:{average_intencity}")
print(f"パワー(周波数領域):{f_power}")