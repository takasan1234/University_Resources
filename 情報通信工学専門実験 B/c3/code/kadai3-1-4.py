import numpy as np
import matplotlib.pyplot as plt

# パラメータ設定
f = 2000  # 信号の周波数 2 kHz
A = np.sqrt(2)  # 振幅
sampling_freqs = np.arange(1000, 10500, 500)  # 1 kHzから10 kHzまで0.5 kHz間隔
peak_freqs = []  # ピーク周波数を格納するリスト
N = 100000

# サンプリング周波数ごとにデータを生成し、フーリエ変換でピークを検出
for fs in sampling_freqs:
    t = np.arange(N)/fs  
    x = A * np.cos(2 * np.pi * f * t)  # 余弦波データ生成
    X = np.fft.fft(x)  # フーリエ変換
    freqs = np.fft.fftfreq(N, 1/fs)  # 周波数インデックス
    
    # 振幅絶対値のピークを検出
    peak_freq = np.abs(freqs[np.argmax(np.abs(X))])
    peak_freqs.append(peak_freq / 1000)  # kHzに変換して保存

# グラフの描画
plt.figure()
plt.plot(sampling_freqs / 1000, peak_freqs, 'bo-')  # サンプリング周波数 vs ピーク周波数
plt.xlabel("Sampling Frequency [kHz]")
plt.ylabel("Peak Frequency [kHz]")
plt.grid()
plt.show()
