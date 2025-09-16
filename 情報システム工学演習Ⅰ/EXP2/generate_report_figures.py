# レポート用図表生成スクリプト
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import linalg
import os

# 出力ディレクトリの作成
os.makedirs('report/figures', exist_ok=True)

# 日本語フォント設定（警告を避けるため）
plt.rcParams['figure.max_open_warning'] = 0
plt.rcParams['font.size'] = 10

# 共通関数の定義
def delay_coordinates(X, w):
    m = len(X)
    mp = int(np.floor(m / w))
    Xw = np.zeros((mp, w))
    for t in range(1, mp+1):
        Xw[t-1,:] = X[(t-1)*w:t*w]
    return Xw

def my_svd(Xw, k):
    [U, s, Vh] = linalg.svd(Xw, full_matrices=False)
    U_k = U[:,0:k]; s_k = s[0:k]; Vh_k = Vh[0:k,:]
    return (U_k, s_k, Vh_k)

def calculate_mse(X_original, X_reconstructed):
    min_len = min(len(X_original), len(X_reconstructed))
    return np.mean((X_original[:min_len] - X_reconstructed[:min_len])**2)

print("=== レポート用図表生成開始 ===")

# ==================== 課題2: 花粉症データ解析 ====================
print("\n1. 課題2用図表生成...")

# 花粉症データの読み込み
try:
    df_kafunsho = pd.read_csv('./data/kafunsho.csv', header=2, index_col=0, parse_dates=True)
    X_kafunsho = df_kafunsho.iloc[:, 0].to_numpy()
    
    # 図1: 花粉症データの時系列プロット
    plt.figure(figsize=(10, 4))
    plt.plot(X_kafunsho, linewidth=2, color='green')
    plt.title('Kafunsho (Hay Fever) Google Trends Data', fontsize=14)
    plt.xlabel('Week')
    plt.ylabel('Search Trend Value')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('report/figures/fig1_kafunsho_timeseries.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 図2: w=12でのSVD分解結果
    w1 = 12
    k = 2
    Xw1 = delay_coordinates(X_kafunsho, w1)
    (U1, s1, Vh1) = my_svd(Xw1, k)
    
    # 元データとウィンドウ分割 + U成分
    plt.figure(figsize=(12, 8))
    colors = ['orange', 'green']
    
    # 上段: 元データとウィンドウ分割
    plt.subplot(3, 1, 1)
    plt.plot(X_kafunsho)
    for t in range(0, len(Xw1)+1):
        plt.axvline(x=t*w1, color='gray', linestyle='dashed', alpha=0.7)
    plt.title(f'Original Data with Window Division (w={w1})')
    plt.xlabel('Time')
    plt.ylabel('Value')
    
    # 中段・下段: U成分
    for i in range(k):
        plt.subplot(3, 1, i+2)
        plt.stem(U1[:,i]*s1[i], linefmt='-', markerfmt='o', basefmt=' ', color=colors[i])
        plt.title(f'Projection Matrix P[{i}] = U[{i}] × s[{i}]')
        plt.xlabel(f'Time Window Index (t=1,...,{len(Xw1)})')
        plt.ylabel('Weight')
    
    plt.tight_layout()
    plt.savefig('report/figures/fig2_kafunsho_svd_w12.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 図3: w=12でのVh局所パターン
    plt.figure(figsize=(10, 4))
    for i in range(k):
        plt.subplot(1, k, i+1)
        plt.plot(Vh1[i,:], 'o-', color=colors[i], linewidth=2, markersize=4)
        plt.title(f'Local Pattern Vh[{i}] (w={w1})')
        plt.xlabel('Position in Window')
        plt.ylabel('Weight')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('report/figures/fig3_kafunsho_vh_w12.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 図4: w=24でのSVD分解結果
    w2 = 24
    Xw2 = delay_coordinates(X_kafunsho, w2)
    (U2, s2, Vh2) = my_svd(Xw2, k)
    
    plt.figure(figsize=(12, 8))
    
    # 上段: 元データとウィンドウ分割
    plt.subplot(3, 1, 1)
    plt.plot(X_kafunsho)
    for t in range(0, len(Xw2)+1):
        plt.axvline(x=t*w2, color='gray', linestyle='dashed', alpha=0.7)
    plt.title(f'Original Data with Window Division (w={w2})')
    plt.xlabel('Time')
    plt.ylabel('Value')
    
    # 中段・下段: U成分
    for i in range(k):
        plt.subplot(3, 1, i+2)
        plt.stem(U2[:,i]*s2[i], linefmt='-', markerfmt='o', basefmt=' ', color=colors[i])
        plt.title(f'Projection Matrix P[{i}] = U[{i}] × s[{i}]')
        plt.xlabel(f'Time Window Index (t=1,...,{len(Xw2)})')
        plt.ylabel('Weight')
    
    plt.tight_layout()
    plt.savefig('report/figures/fig4_kafunsho_svd_w24.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 図5: w=24でのVh局所パターン
    plt.figure(figsize=(10, 4))
    for i in range(k):
        plt.subplot(1, k, i+1)
        plt.plot(Vh2[i,:], 'o-', color=colors[i], linewidth=2, markersize=4)
        plt.title(f'Local Pattern Vh[{i}] (w={w2})')
        plt.xlabel('Position in Window')
        plt.ylabel('Weight')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('report/figures/fig5_kafunsho_vh_w24.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 図6: 再構成結果比較
    plt.figure(figsize=(12, 8))
    
    # w=12での再構成
    U1_k = U1[:, 0:k]; s1_k = s1[0:k]; Vh1_k = Vh1[0:k, :]
    Xw1_rec = np.dot(np.dot(U1_k, np.diag(s1_k)), Vh1_k)
    X1_rec = Xw1_rec.flatten()
    mse1 = calculate_mse(X_kafunsho, X1_rec)
    
    # w=24での再構成
    U2_k = U2[:, 0:k]; s2_k = s2[0:k]; Vh2_k = Vh2[0:k, :]
    Xw2_rec = np.dot(np.dot(U2_k, np.diag(s2_k)), Vh2_k)
    X2_rec = Xw2_rec.flatten()
    mse2 = calculate_mse(X_kafunsho, X2_rec)
    
    # 比較プロット
    plt.subplot(3, 1, 1)
    plt.plot(X_kafunsho, 'k-', linewidth=2, label='Original')
    plt.title('Original Kafunsho Data')
    plt.ylabel('Value')
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.plot(X1_rec, 'r-', linewidth=2)
    plt.title(f'Reconstruction (w={w1}, k={k}, MSE={mse1:.3f})')
    plt.ylabel('Value')
    
    plt.subplot(3, 1, 3)
    plt.plot(X2_rec, 'b-', linewidth=2)
    plt.title(f'Reconstruction (w={w2}, k={k}, MSE={mse2:.3f})')
    plt.xlabel('Time')
    plt.ylabel('Value')
    
    plt.tight_layout()
    plt.savefig('report/figures/fig6_kafunsho_reconstruction.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  課題2図表完了 (MSE比較: w={w1}={mse1:.3f}, w={w2}={mse2:.3f})")
    
except Exception as e:
    print(f"  課題2エラー: {e}")

# ==================== 課題4: 多言語データ解析 ====================
print("\n2. 課題4用図表生成...")

try:
    # 多言語データの読み込み
    languages = ['python', 'java', 'c++']
    lang_data = {}
    
    for lang in languages:
        filename = f'./data/{lang}.csv'
        df = pd.read_csv(filename, header=2, index_col=0, parse_dates=True)
        lang_data[lang] = df.iloc[:, 0].to_numpy()
    
    # 図7: 3言語トレンド比較
    plt.figure(figsize=(12, 8))
    colors = ['blue', 'orange', 'green']
    
    # 個別プロット
    for i, lang in enumerate(languages):
        plt.subplot(2, 2, i+1)
        plt.plot(lang_data[lang], linewidth=2, color=colors[i])
        plt.title(f'{lang.upper()} Google Trends')
        plt.ylabel('Trend Value')
        plt.xlabel('Week')
        plt.grid(True, alpha=0.3)
    
    # 統合比較
    plt.subplot(2, 2, 4)
    for i, lang in enumerate(languages):
        plt.plot(lang_data[lang], linewidth=2, color=colors[i], label=f'{lang.upper()}')
    plt.title('Programming Language Trend Comparison')
    plt.ylabel('Trend Value')
    plt.xlabel('Week')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('report/figures/fig7_multilang_trends.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 多次元SVD解析
    w = 12
    k = 3
    
    # 各言語をdelay coordinates変換
    delay_matrices = []
    for lang in languages:
        Xw = delay_coordinates(lang_data[lang], w)
        delay_matrices.append(Xw)
    
    # 統合行列作成とSVD
    X_stack = np.vstack(delay_matrices)
    (U, s, Vh) = linalg.svd(X_stack, full_matrices=False)
    U_k = U[:, 0:k]; s_k = s[0:k]; Vh_k = Vh[0:k, :]
    
    # 図8: 特異値と寄与率
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.semilogy(s_k, 'ro-', linewidth=2, markersize=8)
    plt.title(f'Singular Values (Top {k})')
    plt.xlabel('Component Index')
    plt.ylabel('Singular Value (Log Scale)')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    contribution_ratio = s_k**2 / np.sum(s_k**2) * 100
    plt.bar(range(len(s_k)), contribution_ratio, color=['red', 'green', 'blue'])
    plt.title('Contribution Ratio of Components')
    plt.xlabel('Component Index')
    plt.ylabel('Contribution Ratio (%)')
    for i, ratio in enumerate(contribution_ratio):
        plt.text(i, ratio + 1, f'{ratio:.1f}%', ha='center')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('report/figures/fig8_multilang_singular_values.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 図9: Vh局所パターン
    plt.figure(figsize=(12, 6))
    
    for i in range(k):
        plt.subplot(2, k, i+1)
        plt.plot(Vh_k[i, :], 'o-', color=colors[i], linewidth=2, markersize=4)
        plt.title(f'Vh[{i}] - Local Pattern')
        plt.xlabel(f'Position in Window (w={w})')
        plt.ylabel('Weight')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, k, k+i+1)
        plt.stem(Vh_k[i, :], linefmt='-', markerfmt='o', basefmt=' ', color=colors[i])
        plt.title(f'Vh[{i}] - Stem Plot')
        plt.xlabel(f'Position in Window (w={w})')
        plt.ylabel('Weight')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('report/figures/fig9_multilang_vh_patterns.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 図10: 言語間相関分析
    # 各言語のU成分を分離
    lang_sizes = [len(dm) for dm in delay_matrices]
    lang_U_components = {}
    
    start_idx = 0
    for i, lang in enumerate(languages):
        end_idx = start_idx + lang_sizes[i]
        lang_U_components[lang] = U_k[start_idx:end_idx, :]
        start_idx = end_idx
    
    # 相関行列計算
    correlations = np.zeros((len(languages), len(languages)))
    for i, lang1 in enumerate(languages):
        for j, lang2 in enumerate(languages):
            corr = np.corrcoef(lang_U_components[lang1][:, 0], 
                             lang_U_components[lang2][:, 0])[0, 1]
            correlations[i, j] = corr
    
    plt.figure(figsize=(10, 8))
    
    # 相関ヒートマップ
    plt.subplot(2, 2, 1)
    im = plt.imshow(correlations, cmap='coolwarm', vmin=-1, vmax=1)
    plt.colorbar(im)
    plt.title('Language Correlation (1st Component)')
    plt.xticks(range(len(languages)), [l.upper() for l in languages])
    plt.yticks(range(len(languages)), [l.upper() for l in languages])
    
    # 相関値表示
    for i in range(len(languages)):
        for j in range(len(languages)):
            plt.text(j, i, f'{correlations[i, j]:.2f}', 
                    ha='center', va='center', 
                    color='black' if abs(correlations[i, j]) < 0.5 else 'white')
    
    # 各言語の重要度
    plt.subplot(2, 2, 2)
    lang_importance = []
    for lang in languages:
        importance = np.mean(np.abs(lang_U_components[lang][:, 0] * s_k[0]))
        lang_importance.append(importance)
    
    plt.bar([l.upper() for l in languages], lang_importance, color=colors)
    plt.title('Language Importance (1st Component)')
    plt.ylabel('Average Absolute Weight')
    plt.grid(True, alpha=0.3)
    
    # 時間パターン比較
    plt.subplot(2, 1, 2)
    for i, lang in enumerate(languages):
        time_pattern = lang_U_components[lang][:, 0] * s_k[0]
        plt.plot(time_pattern, 'o-', linewidth=2, color=colors[i], 
                label=f'{lang.upper()}', markersize=4)
    
    plt.title('Time Patterns by Language (1st Component)')
    plt.xlabel('Time Window')
    plt.ylabel('Weight × Singular Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('report/figures/fig10_multilang_correlation.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 結果サマリー
    print(f"  課題4図表完了")
    print(f"  統合行列サイズ: {X_stack.shape}")
    print(f"  第1成分寄与率: {contribution_ratio[0]:.1f}%")
    mask = np.triu(np.ones_like(correlations, dtype=bool), k=1)
    max_corr_idx = np.unravel_index(np.argmax(correlations * mask), correlations.shape)
    print(f"  最高相関: {languages[max_corr_idx[0]].upper()}-{languages[max_corr_idx[1]].upper()} ({correlations[max_corr_idx]:.3f})")
    
except Exception as e:
    print(f"  課題4エラー: {e}")

print("\n=== 図表生成完了 ===")
print("生成された図表:")
print("- fig1_kafunsho_timeseries.pdf")
print("- fig2_kafunsho_svd_w12.pdf") 
print("- fig3_kafunsho_vh_w12.pdf")
print("- fig4_kafunsho_svd_w24.pdf")
print("- fig5_kafunsho_vh_w24.pdf")
print("- fig6_kafunsho_reconstruction.pdf")
print("- fig7_multilang_trends.pdf")
print("- fig8_multilang_singular_values.pdf")
print("- fig9_multilang_vh_patterns.pdf")
print("- fig10_multilang_correlation.pdf") 