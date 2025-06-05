#!/bin/bash

echo "全サンプル画像の処理を開始します..."
echo "実行日時: $(date)" > results/processing_summary.txt
echo "" >> results/processing_summary.txt

for i in {1..13}; do
    echo "Processing sample${i}.pgm..."
    
    # エッジ強調のみ
    echo "  - エッジ強調処理中..."
    ./sample edge sampleimages/sample${i}.pgm results/edge_enhanced/sample${i}_edge.pgm
    
    # 二値化のみ（閾値を記録）
    echo "  - 二値化処理中..."
    echo "=== sample${i}.pgm 二値化処理 ===" >> results/processing_summary.txt
    ./sample binary sampleimages/sample${i}.pgm results/binarized/sample${i}_binary.pgm >> results/processing_summary.txt 2>&1
    
    # エッジ強調→二値化（閾値を記録）
    echo "  - エッジ強調→二値化処理中..."
    echo "=== sample${i}.pgm エッジ強調→二値化処理 ===" >> results/processing_summary.txt
    ./sample both sampleimages/sample${i}.pgm results/combined/sample${i}_combined.pgm >> results/processing_summary.txt 2>&1
    
    echo "" >> results/processing_summary.txt
    echo "sample${i}.pgm 処理完了"
done

echo ""
echo "全ての処理が完了しました！"
echo "結果は以下のフォルダに保存されています："
echo "  - results/edge_enhanced/     エッジ強調のみ"
echo "  - results/binarized/         二値化のみ"
echo "  - results/combined/          エッジ強調→二値化"
echo "  - results/processing_summary.txt  閾値情報" 