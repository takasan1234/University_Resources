import matplotlib.pyplot as plt
import pandas as pd
import sys

def visualize_clustering(filename):
    # データの読み込み
    df = pd.read_csv(filename, header=None)
    
    # カラム名の設定（列数に応じて動的に設定）
    if len(df.columns) == 3:
        df.columns = ['x', 'y', 'cluster']
        df['is_outlier'] = 0  # 外れ値フラグがない場合は全て0とする
    else:
        df.columns = ['x', 'y', 'cluster', 'is_outlier']
    
    # プロットの設定
    plt.figure(figsize=(10, 8))
    
    # フォントサイズの設定
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['legend.fontsize'] = 12
    
    # 各クラスタのデータをプロット
    for cluster in df['cluster'].unique():
        # 外れ値ではないデータ
        normal_data = df[(df['cluster'] == cluster) & (df['is_outlier'] == 0)]
        plt.scatter(normal_data['x'], normal_data['y'], 
                   label=f'Cluster {cluster}',
                   alpha=0.6,  # 透明度を設定
                   s=100)      # マーカーサイズを大きく
    
    # 外れ値を別の形状でプロット
    outliers = df[df['is_outlier'] == 1]
    if not outliers.empty:
        plt.scatter(outliers['x'], outliers['y'], 
                   color='red', 
                   marker='*', 
                   s=200, 
                   label='Outliers', 
                   edgecolors='black',
                   linewidth=1.5)
    
    # タイトルをファイル名に基づいて設定
    if 'DBSCAN' in filename:
        plt.title('DBSCAN Clustering Results')
    else:
        plt.title('K-means Clustering Results')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(frameon=True, fancybox=True, shadow=True)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 余白の調整
    plt.tight_layout()
    
    # PDFとして保存（高解像度）
    output_pdf = filename.replace('.csv', '_plot.pdf')
    plt.savefig(output_pdf, 
                format='pdf',
                dpi=300,
                bbox_inches='tight',
                pad_inches=0.1)
    print(f"Plot saved as {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualize.py <clustering_output.csv>")
        sys.exit(1)
    
    visualize_clustering(sys.argv[1]) 