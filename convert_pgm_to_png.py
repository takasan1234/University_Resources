#!/usr/bin/env python3
"""
PGMファイルをPNG形式に変換するスクリプト
"""

import os
import glob
from PIL import Image

def convert_pgm_to_png():
    """PGMファイルをPNG形式に変換"""
    
    # 対象フォルダ
    source_folders = ['results/binarized', 'results/combined', 'results/edge_enhanced']
    output_folder = 'images'
    
    # 出力フォルダが存在しない場合は作成
    os.makedirs(output_folder, exist_ok=True)
    
    total_converted = 0
    
    for folder in source_folders:
        if not os.path.exists(folder):
            print(f"フォルダが見つかりません: {folder}")
            continue
            
        # フォルダ名を取得（binarized, combined, edge_enhanced）
        folder_name = os.path.basename(folder)
        
        # PGMファイルを検索
        pgm_files = glob.glob(os.path.join(folder, '*.pgm'))
        
        print(f"\n=== {folder} フォルダの処理 ===")
        print(f"見つかったPGMファイル数: {len(pgm_files)}")
        
        for pgm_file in pgm_files:
            try:
                # ファイル名を取得（拡張子なし）
                base_name = os.path.splitext(os.path.basename(pgm_file))[0]
                
                # 出力ファイル名を作成（フォルダ名を接頭辞として追加）
                png_filename = f"{folder_name}_{base_name}.png"
                png_path = os.path.join(output_folder, png_filename)
                
                # PGMファイルを開いてPNGとして保存
                with Image.open(pgm_file) as img:
                    # PGMファイルをPNG形式で保存
                    img.save(png_path, 'PNG')
                    
                print(f"変換完了: {pgm_file} -> {png_path}")
                total_converted += 1
                
            except Exception as e:
                print(f"エラー: {pgm_file} の変換に失敗しました - {e}")
    
    print(f"\n=== 変換完了 ===")
    print(f"総変換ファイル数: {total_converted}")
    print(f"出力フォルダ: {output_folder}")

if __name__ == "__main__":
    convert_pgm_to_png() 