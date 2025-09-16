# 課題4-3: 複数キーワードの多次元時系列に対するSVD解析
# プログラミング言語（Python, Java, C++）のGoogle Trendsデータ解析

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import linalg

# 表示設定
np.set_printoptions(precision=2, suppress=True)

# 既存関数の定義（ノートブックから）
def delay_coordinates(X, w):
    """部分シーケンス行列 (delay coordinates matrix) を作成"""
    m = len(X)
    mp = int(np.floor(m / w))
    Xw = np.zeros((mp, w))
    for t in range(1, mp+1):
        Xw[t-1,:] = X[(t-1)*w:t*w]
    return Xw

def my_svd(Xw, k):
    """SVD分解と上位k成分抽出"""
    [U, s, Vh] = linalg.svd(Xw, full_matrices=False)
    U_k = U[:,0:k]; s_k = s[0:k]; Vh_k = Vh[0:k,:]
    return (U_k, s_k, Vh_k)

# ========== ステップ1: データ読み込み ==========
print("=== 課題4-3: 複数キーワード多次元SVD解析 ===")

languages = ['python', 'java', 'c++']
lang_data = {}
lang_dataframes = {}

print("\n1. 各言語データの読み込み:")
for lang in languages:
    filename = f'./data/{lang}.csv'
    df = pd.read_csv(filename, header=2, index_col=0, parse_dates=True)
    lang_dataframes[lang] = df
    lang_data[lang] = df.iloc[:, 0].to_numpy()
    print(f"  {lang.upper()}: 形状{lang_data[lang].shape}, 範囲[{lang_data[lang].min()}, {lang_data[lang].max()}]")

# ========== ステップ2: 多次元SVD解析関数 ==========
def svd_multi_decomp(data_dict, w, k, lang_names):
    """複数時系列データに対してSVDを行い、共通パターンを抽出"""
    print(f"\n2. 多次元SVD解析 (w={w}, k={k}):")
    
    # 各時系列をdelay coordinates行列に変換
    delay_matrices = []
    for lang in lang_names:
        Xw = delay_coordinates(data_dict[lang], w)
        delay_matrices.append(Xw)
        print(f"  {lang.upper()}: X{data_dict[lang].shape} -> Xw{Xw.shape}")
    
    # 縦方向に連結（スタック）
    X_stack = np.vstack(delay_matrices)
    print(f"  統合行列: {X_stack.shape}")
    
    # SVD分解
    (U, s, Vh) = linalg.svd(X_stack, full_matrices=False)
    U_k = U[:, 0:k]; s_k = s[0:k]; Vh_k = Vh[0:k, :]
    
    print(f"  SVD結果: U{U_k.shape}, s{s_k.shape}, Vh{Vh_k.shape}")
    print(f"  上位{k}成分の特異値: {s_k}")
    print(f"  寄与率: {s_k**2 / np.sum(s_k**2) * 100}%")
    
    return U_k, s_k, Vh_k, X_stack, delay_matrices

# ========== ステップ3: SVD解析実行 ==========
w = 12  # ウィンドウサイズ（3ヶ月）
k = 3   # 上位3成分

U_k, s_k, Vh_k, X_stack, delay_matrices = svd_multi_decomp(lang_data, w, k, languages)

# ========== ステップ4: 結果可視化 ==========
print("\n3. 可視化結果:")

# 図1: 元データ比較
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
colors = ['blue', 'orange', 'green']
for i, lang in enumerate(languages):
    plt.plot(lang_data[lang], linewidth=2, color=colors[i], label=f'{lang.upper()}')
plt.title('プログラミング言語トレンド比較')
plt.ylabel('トレンド値')
plt.xlabel('週')
plt.legend()
plt.grid(True, alpha=0.3)

# 図2: 特異値
plt.subplot(2, 2, 2)
plt.semilogy(s_k, 'ro-', linewidth=2, markersize=8)
plt.title(f'特異値（上位{k}個）')
plt.xlabel('成分番号')
plt.ylabel('特異値（対数スケール）')
plt.grid(True, alpha=0.3)

# 図3: 局所パターン（Vh）
for i in range(min(k, 2)):  # 上位2成分のみ表示
    plt.subplot(2, 2, 3+i)
    plt.plot(Vh_k[i, :], 'o-', linewidth=2, markersize=4)
    plt.title(f'Vh[{i}] - 局所パターン')
    plt.xlabel(f'時間窓内位置 (w={w})')
    plt.ylabel('重み')
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ========== ステップ5: 言語間分析 ==========
print("\n4. 言語間分析:")

# 各言語のU成分を分離
lang_sizes = [len(dm) for dm in delay_matrices]
lang_U_components = {}

start_idx = 0
for i, lang in enumerate(languages):
    end_idx = start_idx + lang_sizes[i]
    lang_U_components[lang] = U_k[start_idx:end_idx, :]
    start_idx = end_idx

# 言語間相関分析（第1成分）
correlations = np.zeros((len(languages), len(languages)))
for i, lang1 in enumerate(languages):
    for j, lang2 in enumerate(languages):
        if len(lang_U_components[lang1][:, 0]) > 0 and len(lang_U_components[lang2][:, 0]) > 0:
            corr = np.corrcoef(lang_U_components[lang1][:, 0], 
                             lang_U_components[lang2][:, 0])[0, 1]
            correlations[i, j] = corr

# 言語間相関の可視化
plt.figure(figsize=(8, 6))
plt.subplot(1, 2, 1)
im = plt.imshow(correlations, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(im)
plt.title('言語間相関（第1成分）')
plt.xticks(range(len(languages)), [l.upper() for l in languages])
plt.yticks(range(len(languages)), [l.upper() for l in languages])

# 相関値を表示
for i in range(len(languages)):
    for j in range(len(languages)):
        plt.text(j, i, f'{correlations[i, j]:.2f}', 
                ha='center', va='center', 
                color='black' if abs(correlations[i, j]) < 0.5 else 'white')

# 寄与率
plt.subplot(1, 2, 2)
contribution_ratio = s_k**2 / np.sum(s_k**2) * 100
plt.bar(range(len(s_k)), contribution_ratio, color=['red', 'green', 'blue'])
plt.title('各成分の寄与率')
plt.xlabel('成分番号')
plt.ylabel('寄与率 (%)')
for i, ratio in enumerate(contribution_ratio):
    plt.text(i, ratio + 1, f'{ratio:.1f}%', ha='center')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ========== 結果サマリー ==========
print("\n=== 課題4-3 解析結果サマリー ===")
print(f"• 統合行列サイズ: {X_stack.shape}")
print(f"• 第1成分寄与率: {contribution_ratio[0]:.1f}%")

# 最も類似した言語ペア
mask = np.triu(np.ones_like(correlations, dtype=bool), k=1)
max_corr_idx = np.unravel_index(np.argmax(correlations * mask), correlations.shape)
print(f"• 最も類似: {languages[max_corr_idx[0]].upper()} - {languages[max_corr_idx[1]].upper()}")
print(f"  相関係数: {correlations[max_corr_idx]:.3f}")

print("\n【考察】")
print("• 第1成分: 3言語共通の主要トレンドパターンを抽出")
print("• 言語間相関: 技術トレンドの類似性と独自性を定量化")
print("• SVD多次元解析: 複数時系列の横断的パターン発見に有効")
print("• 実装成果: delay coordinates スタッキング手法の成功")

print("\n課題4-3が完了しました！") 