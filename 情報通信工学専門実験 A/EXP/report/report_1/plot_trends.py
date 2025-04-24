import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# japanize_matplotlibを使用せず、日本語フォントを直接設定
plt.rcParams['font.family'] = 'sans-serif'  # フォントファミリーをサンセリフに設定

# CSVファイルの読み込み
df = pd.read_csv('multiTimeline.csv', skiprows=2)

# 日付を解析
df['月'] = pd.to_datetime(df['月'])

# プロットの作成
plt.figure(figsize=(10, 5))
plt.plot(df['月'], df['DBSCAN: (すべての国)'], label='DBSCAN', linewidth=2)
plt.plot(df['月'], df['k-means: (すべての国)'], label='k-means', linewidth=2)

# グラフの装飾
plt.title('Google Trends: Search Trends (2004-2025)')
plt.xlabel('Year')
plt.ylabel('Search Volume (Relative)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# x軸の日付フォーマットを設定
plt.gca().xaxis.set_major_locator(mdates.YearLocator(3))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# グラフの保存
plt.tight_layout()
plt.savefig('trends_comparison.pdf')
plt.savefig('trends_comparison.png', dpi=300)

print("グラフが保存されました。") 