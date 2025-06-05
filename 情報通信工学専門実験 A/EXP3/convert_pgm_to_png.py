#!/usr/bin/env python3
"""
PGMファイルをPNG形式に変換するスクリプト
"""

import os
import glob
from PIL import Image

def convert_results_pgm_to_png():
    """処理結果のPGMファイルをPNG形式に変換"""
    
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
    
    return total_converted

def convert_sampleimages_pgm_to_png():
    """sampleimagesフォルダのPGMファイルをPNG形式に変換"""
    
    source_folder = 'sampleimages'
    output_folder = 'sampleimages'  # 同じフォルダに出力
    
    total_converted = 0
    
    if not os.path.exists(source_folder):
        print(f"フォルダが見つかりません: {source_folder}")
        return 0
    
    # PGMファイルを検索
    pgm_files = glob.glob(os.path.join(source_folder, '*.pgm'))
    
    print(f"\n=== {source_folder} フォルダの処理 ===")
    print(f"見つかったPGMファイル数: {len(pgm_files)}")
    
    for pgm_file in pgm_files:
        try:
            # ファイル名を取得（拡張子なし）
            base_name = os.path.splitext(os.path.basename(pgm_file))[0]
            
            # 出力ファイル名を作成（同じフォルダにPNGとして保存）
            png_filename = f"{base_name}.png"
            png_path = os.path.join(output_folder, png_filename)
            
            # PGMファイルを開いてPNGとして保存
            with Image.open(pgm_file) as img:
                # PGMファイルをPNG形式で保存
                img.save(png_path, 'PNG')
                
            print(f"変換完了: {pgm_file} -> {png_path}")
            total_converted += 1
            
        except Exception as e:
            print(f"エラー: {pgm_file} の変換に失敗しました - {e}")
    
    return total_converted

def convert_pgm_to_png():
    """全てのPGMファイルをPNG形式に変換"""
    
    print("PGMファイルをPNG形式に変換します...")
    
    # 処理結果の変換
    results_converted = convert_results_pgm_to_png()
    
    # サンプル画像の変換
    samples_converted = convert_sampleimages_pgm_to_png()
    
    total_converted = results_converted + samples_converted
    
    print(f"\n=== 全体の変換完了 ===")
    print(f"処理結果ファイル数: {results_converted}")
    print(f"サンプル画像ファイル数: {samples_converted}")
    print(f"総変換ファイル数: {total_converted}")

if __name__ == "__main__":
    convert_pgm_to_png() 