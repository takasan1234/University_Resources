# クワイン・マクラスキー法 + Petrick's Method による最小SOP導出 (デバッグ版)
import time
import logging
import random

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def count_ones(term):
    """各ビット列に含まれる1の数を数える"""
    return term.count("1")

def combine_terms(a, b):
    """2つのビット列を比較し、1ビットのみ異なる場合に結合（'-'を用いる）"""
    diff = 0
    combined = []
    for bit_a, bit_b in zip(a, b):
        if bit_a != bit_b:
            diff += 1
            combined.append('-')
        else:
            combined.append(bit_a)
    return ''.join(combined) if diff == 1 else None

def initial_grouping(minterms):
    """最小項を1の数に基づいて分類する"""
    groups = {}
    for term in minterms:
        ones = count_ones(term)
        groups.setdefault(ones, []).append(term)
    
    logger.info(f"初期グループ化完了: {len(groups)} グループ")
    for ones, terms in groups.items():
        logger.info(f"  1の数{ones}: {len(terms)}項")
    
    return groups

def combine_groups(groups):
    """隣接グループの項を1ビット異なるもの同士で結合する"""
    new_groups = {}
    marked = set()
    keys = sorted(groups)
    
    combinations_checked = 0
    combinations_combined = 0
    
    for i in range(len(keys) - 1):
        for a in groups[keys[i]]:
            for b in groups[keys[i + 1]]:
                combinations_checked += 1
                combined = combine_terms(a, b)
                if combined:
                    combinations_combined += 1
                    new_groups.setdefault(count_ones(combined.replace('-', '0')), []).append(combined)
                    marked.update([a, b])
    
    logger.info(f"結合処理: {combinations_checked}通り検査, {combinations_combined}通り結合")
    return new_groups, marked

def quine_mccluskey(minterms):
    """Prime Implicant を列挙するメイン手続き"""
    logger.info(f"クワイン・マクラスキー法開始: {len(minterms)} 最小項")
    
    # 初期グループ化
    groups = initial_grouping(minterms)
    prime_implicants = set()
    iteration = 0

    # グループが空になるまで繰り返し
    while groups:
        iteration += 1
        logger.info(f"--- イテレーション {iteration} ---")
        
        # 隣接グループの結合
        start_time = time.time()
        new_groups, marked = combine_groups(groups)
        combine_time = time.time() - start_time
        
        # マークされていない項を素項として追加
        new_primes = 0
        for group in groups.values():
            for term in group:
                if term not in marked:
                    prime_implicants.add(term)
                    new_primes += 1
        
        logger.info(f"結合時間: {combine_time:.4f}秒, 新規素項: {new_primes}個")
        
        # 新しいグループを次のイテレーション用に設定
        groups = new_groups
        
        if not groups:
            logger.info("結合可能な項がなくなりました")

    logger.info(f"素項発見完了: {len(prime_implicants)}個")
    return sorted(prime_implicants)

def petricks_method(minterms, implicants):
    """Petrickの方法で最小カバーの組み合わせを選出 (デバッグ版)"""
    logger.info(f"Petrick's Method開始: {len(minterms)}最小項, {len(implicants)}素項")
    
    # 各最小項がカバーされる PI のインデックスを記録
    table = {m: [] for m in minterms}
    coverage_count = 0
    
    for i, imp in enumerate(implicants):
        for m in minterms:
            if all(a == '-' or a == b for a, b in zip(imp, m)):
                table[m].append(i)
                coverage_count += 1
    
    logger.info(f"カバレッジテーブル作成完了: {coverage_count}個の関係")
    
    # カバレッジ統計
    essential_pis = []
    for m, covering_pis in table.items():
        if len(covering_pis) == 0:
            logger.warning(f"最小項 {m} をカバーする素項がありません")
        elif len(covering_pis) == 1:
            logger.info(f"必須素項発見: PI[{covering_pis[0]}] = {implicants[covering_pis[0]]}")
            essential_pis.append(covering_pis[0])

    def distribute(a, b):
        """AND×OR の分配によって組み合わせを展開"""
        result = []
        operations = 0
        for x in a:
            for y in b:
                operations += 1
                merged = sorted(set(x).union([y]))
                if merged not in result:
                    result.append(merged)
                
                # 進捗ログ（大量の組み合わせの場合）
                if operations % 100000 == 0:
                    logger.info(f"分配処理中: {operations}回実行, 現在の解候補: {len(result)}個")
                
                # 異常に多くなった場合の制限
                if len(result) > 200000:
                    logger.warning(f"解候補が{len(result)}個に達しました。処理を制限します。")
                    return result[:100000]  # 上位100000個に制限
        
        logger.info(f"分配完了: {operations}回実行, 最終解候補: {len(result)}個")
        return result

    # 初期化（1つ目の最小項）
    logger.info("分配法開始...")
    product = [[i] for i in table[minterms[0]]]
    logger.info(f"初期状態: {len(product)}個の解候補")
    
    for idx, m in enumerate(minterms[1:], 1):
        logger.info(f"最小項 {idx}/{len(minterms)-1} 処理中...")
        start_time = time.time()
        product = distribute(product, table[m])
        distribute_time = time.time() - start_time
        logger.info(f"処理時間: {distribute_time:.4f}秒, 現在の解候補: {len(product)}個")
        
        # メモリ使用量が異常に多い場合の警告
        if len(product) > 50000:
            logger.warning(f"解候補数が{len(product)}個に増加。計算が困難になる可能性があります。")

    # 最小項数を持つものを選択
    if not product:
        logger.error("有効な解が見つかりませんでした")
        return []
    
    min_len = min(len(p) for p in product)
    best_solutions = [p for p in product if len(p) == min_len]
    logger.info(f"最適解発見: 最小項数={min_len}, 解の数={len(best_solutions)}個")
    
    best = best_solutions[0]
    return [implicants[i] for i in best]

def generate_test_case(bits, density=0.5):
    """指定ビット数のテストケース生成"""
    total_combinations = 2 ** bits
    num_minterms = max(1, int(total_combinations * density))
    
    # ランダムに最小項を選択
    all_terms = [format(i, f'0{bits}b') for i in range(total_combinations)]
    minterms = random.sample(all_terms, num_minterms)
    
    logger.info(f"{bits}ビットテストケース生成: {len(minterms)}/{total_combinations} 最小項")
    return sorted(minterms)

def run_complexity_test():
    """計算複雑性テスト実行"""
    results = []
    
    for bits in [5, 6, 7, 8]:
        logger.info(f"\n{'='*50}")
        logger.info(f"  {bits}ビット計算複雑性テスト開始")
        logger.info(f"{'='*50}")
        
        # テストケース生成
        random.seed(42)  # 再現性のため
        minterms = generate_test_case(bits, density=0.4)  # 40%の密度
        
        # 全体の開始時間
        total_start = time.time()
        
        # QMC実行
        logger.info("--- Quine-McCluskey 実行開始 ---")
        qmc_start = time.time()
        try:
            implicants = quine_mccluskey(minterms)
            qmc_time = time.time() - qmc_start
            logger.info(f"QMC完了: {qmc_time:.4f}秒, 素項数: {len(implicants)}")
        except Exception as e:
            logger.error(f"QMC実行エラー: {e}")
            continue
        
        # Petrick's Method実行
        logger.info("--- Petrick's Method 実行開始 ---")
        petrick_start = time.time()
        try:
            minimized = petricks_method(minterms, implicants)
            petrick_time = time.time() - petrick_start
            logger.info(f"Petrick完了: {petrick_time:.4f}秒, 最小項数: {len(minimized)}")
        except Exception as e:
            logger.error(f"Petrick実行エラー: {e}")
            petrick_time = float('inf')
            minimized = []
        
        total_time = time.time() - total_start
        
        # 結果記録
        result = {
            'bits': bits,
            'minterms_count': len(minterms),
            'prime_implicants_count': len(implicants),
            'qmc_time': qmc_time,
            'petrick_time': petrick_time,
            'total_time': total_time,
            'final_terms': len(minimized)
        }
        results.append(result)
        
        logger.info(f"{bits}ビットテスト完了: 総時間 {total_time:.4f}秒")
        
        # 長時間になる場合は中断判定
        if petrick_time > 600:  # 10分以上
            logger.warning("計算時間が長すぎるため、これ以上のビット数テストを中断します")
            break
    
    # 結果サマリー
    logger.info(f"\n{'='*60}")
    logger.info("  計算複雑性テスト結果サマリー")
    logger.info(f"{'='*60}")
    logger.info(f"{'ビット':<6} {'最小項':<8} {'素項':<6} {'QMC時間':<10} {'Petrick時間':<12} {'総時間':<10}")
    logger.info("-" * 60)
    
    for r in results:
        logger.info(f"{r['bits']:<6} {r['minterms_count']:<8} {r['prime_implicants_count']:<6} "
                   f"{r['qmc_time']:<10.4f} {r['petrick_time']:<12.4f} {r['total_time']:<10.4f}")
    
    return results

# テスト実行
if __name__ == "__main__":
    logger.info("クワイン・マクラスキー法 計算複雑性テスト開始")
    results = run_complexity_test()
    logger.info("全テスト完了") 