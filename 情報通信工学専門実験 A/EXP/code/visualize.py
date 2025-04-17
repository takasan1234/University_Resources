import matplotlib.pyplot as plt
import pandas as pd
import sys

def visualize_clustering(filename):
    # データの読み込み
    df = pd.read_csv(filename, header=None, names=['x', 'y', 'cluster'])
    
    # プロットの設定
    plt.figure(figsize=(10, 8))
    
    # 各クラスタのデータをプロット
    for cluster in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster]
        plt.scatter(cluster_data['x'], cluster_data['y'], label=f'Cluster {cluster}')
    
    plt.title('K-means Clustering Results')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    
    # 画像として保存
    output_image = filename.replace('.csv', '_plot.png')
    plt.savefig(output_image)
    print(f"Plot saved as {output_image}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualize.py <clustering_output.csv>")
        sys.exit(1)
    
    visualize_clustering(sys.argv[1]) 