import numpy as np
import matplotlib.pyplot as plt

# サンプリング周波数とサンプル数の設定
fs = 10 # kHz
N = 100000 # サンプル数

# 雑音の分散
n_var = 1

# 時間インデックスの生成 (単位: ms)
t_index = np.arange(N)*1/fs # msec

# 平均0、分散1の白色ガウス雑音を生成
t_noise = np.random.normal(0.0, np.sqrt(n_var), N)

# 時間領域での強度、エネルギー、パワーの計算
t_intensity = t_noise * t_noise # 強度 = 雑音の振幅の二乗
t_energy = (t_intensity * 1/fs).sum() # エネルギー = 強度の積分
t_power = t_energy / (N * 1/fs) # パワー = エネルギーを時間で割る

# 周波数インデックスの生成
f_index = np.fft.fftfreq(N, 1/fs)

# 雑音をフーリエ変換
f_noise = np.fft.fft(t_noise)

# ローパスフィルタの設定 (帯域幅 W = 5 kHz)
LPF_width = np.float64(5) # フィルタの帯域幅
f_LPF = np.complex128(np.abs(f_index) <= LPF_width/2) # フィルタの周波数領域でのマスク

# フィルタを適用した雑音の周波数領域データ
f_noise_LPF = f_LPF * f_noise

# フィルタ後の雑音を時間領域に戻す
t_noise_LPF = np.fft.ifft(f_noise_LPF).real

# パワーの計算 (時間領域での平均二乗値)
power = np.mean(t_noise ** 2)

# ここに本来、白色ガウス雑音サンプルの時間波形 (左) とヒストグラム (右)が生成されるコードがあります。


# フィルタ適用前のスペクトルをプロット
plt.figure()
plt.plot()
plt.xlim([-5, 5])
plt.ylim([0, 0.014])
plt.plot(np.fft.fftshift(f_index), np.fft.fftshift(np.abs(f_noise))/100000, "b", label="Before LPF")
plt.xlabel("Frequency[kHz]")
plt.text(-4.8, 1350, "before LPF", fontsize=15)
plt.ylabel("Amptitude", fontsize=10)
plt.legend(loc="upper right")
plt.show()

# フィルタ適用後のスペクトルをプロット
plt.figure()
plt.plot()
plt.xlim([-5, 5])
plt.ylim([0, 0.014])
plt.plot(np.fft.fftshift(f_index), np.fft.fftshift(np.abs(f_noise_LPF))/100000, "b", label="After LPF")
plt.xlabel("Frequency[kHz]")
plt.ylabel("Amptitude", fontsize=10)
plt.text(-4.8, 1350, "after LPF", fontsize=15)
plt.legend(loc="upper right")
plt.show()

# 時間領域とヒストグラムのプロット
plt.figure(figsize=[15,8])
plt.subplots_adjust(wspace=0.05, hspace=0.1)

# (a) フィルタ適用前の時間領域雑音
plt.subplot(221)
plt.xlim([0, 5])
plt.ylim([-5, 5])
plt.plot(t_index, t_noise, "bo--")
plt.hlines([0], 0, 5, "black", linewidth=0.5, linestyles='--', label="original noise")
plt.text(-0.7, -8, "Amptitude", rotation=90, fontsize=15)
plt.legend(loc="upper right")
plt.text(0.04, 4.3, "(a)", fontsize=15)

# (b) フィルタ適用前のヒストグラムと理論ガウス分布
x = np.arange(-5, 5, 0.01)
gauss = 1/np.sqrt(2*np.pi*n_var)*np.exp(-x*x/(2*n_var))
plt.subplot(222)
plt.xlim([0, 0.6])
plt.ylim([-5, 5])
plt.hist(t_noise, bins=100, density=True, color="lightsteelblue", orientation="horizontal")
plt.plot(gauss, x, "m--", label="N₀(0, 1)")
plt.legend(loc="upper right")
plt.text(0.01, 4.3, "(b)", fontsize=15)

# (c) フィルタ適用後の時間領域雑音
plt.subplot(223)
plt.xlim([0, 5])
plt.ylim([-5, 5])
plt.plot(t_index, t_noise_LPF, "bo--")
plt.hlines([0], 0, 5, "black", linewidth=0.5, linestyles='--', label="noise After LPF")
plt.xlabel("Time[ms]", fontsize=15)
plt.legend(loc="upper right")
plt.text(0.04, 4.3, "(c)", fontsize=15)

# (d) フィルタ適用後のヒストグラムと理論ガウス分布
x = np.arange(-5, 5, 0.01)
gauss = 1/np.sqrt(2*np.pi*n_var/2)*np.exp(-x*x/(2*n_var/2))
plt.subplot(224)
plt.xlim([0, 0.6])
plt.ylim([-5, 5])
plt.hist(t_noise_LPF, bins=100, density=True, color="lightsteelblue", orientation="horizontal")
plt.plot(gauss, x, "m--", label="N₀(0, 0.5)")
plt.legend(loc="upper right")
plt.xlabel("Proba density func", fontsize=15)
plt.text(0.01, 4.3, "(d)", fontsize=10)
plt.show()

# フィルタ適用前後の比較プロット
plt.figure(figsize=[15,5])
plt.subplots_adjust(wspace=0.08, hspace=0.1)

# (a) フィルタ適用前の時間領域雑音
plt.subplot(121)
plt.xlim([0, 5])
plt.ylim([-5, 5])
plt.plot(t_index, t_noise, "bo--")
plt.hlines([0], 0, 5, "black", linewidth=0.5, linestyles='--')
plt.text(0.1, 4.3, "(a)", fontsize=15)
plt.xlabel("Time[ms]", fontsize=15)
plt.ylabel("Amptitude", fontsize=15)

# (b) フィルタ適用前のヒストグラムと理論ガウス分布
x = np.arange(-5, 5, 0.01)
gauss = 1/np.sqrt(2*np.pi*n_var)*np.exp(-x*x/(2*n_var))
plt.subplot(122)
plt.xlim([0, 0.6])
plt.ylim([-5, 5])
plt.hist(t_noise, bins=100, density=True, color="lightsteelblue", orientation="horizontal")
plt.plot(gauss, x, "m--", label="N₀(0, 1)")
plt.text(0.01, 4.3, "(b)", fontsize=15)
plt.xlabel("Proba density func", fontsize=15)
plt.legend(loc="upper right")
plt.show()

# パワーの表示
print(f"計算されたパワー: {power:.3f}")