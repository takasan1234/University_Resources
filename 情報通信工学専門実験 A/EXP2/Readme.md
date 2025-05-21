# 経路選択アルゴリズムの実装と評価

このプロジェクトは、情報通信工学専門実験Aにおける経路選択アルゴリズムの実装と評価を行うためのものです。

## 実装内容

以下の6種類の経路選択アルゴリズムを実装しています：
1. 最小ホップ経路を用いた固定経路（Dijkstraアルゴリズム）
2. 最大路を用いた固定経路
3. 最小ホップを用いた要求時経路
4. 最大路を用いた要求時経路
5. 空き容量の逆数を考慮した経路
6. 最短最大路（Shortest Widest Path）

## 環境構築

### 必要条件
- Java Development Kit (JDK)
- Python 3.8以上
- pip（Pythonパッケージマネージャー）

### Pythonの仮想環境設定(採点の際には必要ありません)

1. 仮想環境の作成
```bash
python -m venv .venv
```

2. 仮想環境の有効化
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. 必要なパッケージのインストール
```bash
pip install -r requirements.txt
```

## 実行手順

### 1. Javaプログラムの実行

1. Javaファイルのコンパイル
```bash
javac dijkstra.java
```

2. プログラムの実行
```bash
java dijkstra
```

### 2. グラフの生成(採点の際には必要ありません。すでにグラフは添付済みです。)

1. シミュレーション結果の可視化
```bash
python plot_graph.py
```

生成されるグラフ：
- 各経路選択アルゴリズムの呼損率比較
- 異なるλ値に対する性能評価結果
- 最小ホップ固定経路の詳細分析

## ファイル構成

- `dijkstra.java`: 経路選択アルゴリズムの実装
- `plot_graph.py`: 結果の可視化スクリプト
- `distance.txt`: ネットワークトポロジー定義ファイル
- `requirements.txt`: Pythonパッケージ依存関係
- `report/`: レポートおよび生成されたグラフの保存ディレクトリ