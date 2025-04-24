from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

def create_trends_html():
    html_content = """
    <html>
    <head>
        <script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/4031_RC01/embed_loader.js"></script>
    </head>
    <body>
        <script type="text/javascript">
            trends.embed.renderExploreWidget("TIMESERIES", {
                "comparisonItem":[
                    {"keyword":"DBSCAN","geo":"","time":"2004-01-01 2025-04-24"},
                    {"keyword":"k-means","geo":"","time":"2004-01-01 2025-04-24"}
                ],
                "category":0,
                "property":""
            }, {
                "exploreQuery":"date=all&q=DBSCAN,k-means&hl=ja",
                "guestPath":"https://trends.google.co.jp:443/trends/embed/"
            });
        </script>
    </body>
    </html>
    """
    
    with open("trends.html", "w") as f:
        f.write(html_content)

def capture_trends_to_pdf():
    # ChromeOptionsの設定
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモードで実行
    chrome_options.add_argument("--window-size=1920,1080")
    
    # WebDriverの初期化
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # HTMLファイルのパスを取得
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "trends.html")
        file_url = f"file://{html_path}"
        
        # ページを開く
        driver.get(file_url)
        
        # グラフの読み込みを待機
        time.sleep(5)  # グラフの描画を待つ
        
        # スクリーンショットを保存
        driver.save_screenshot("google_trends.png")
        
        print("Google Trendsのグラフを保存しました。")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    create_trends_html()
    capture_trends_to_pdf()
