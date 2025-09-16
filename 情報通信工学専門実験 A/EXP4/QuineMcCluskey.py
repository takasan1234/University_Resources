# クワイン・マクラスキー法 + Petrick's Method による最小SOP導出


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
    return groups


def combine_groups(groups):
    """隣接グループの項を1ビット異なるもの同士で結合する"""
    new_groups = {}
    marked = set()
    keys = sorted(groups)
    for i in range(len(keys) - 1):
        for a in groups[keys[i]]:
            for b in groups[keys[i + 1]]:
                combined = combine_terms(a, b)
                if combined:
                    new_groups.setdefault(count_ones(combined.replace('-', '0')), []).append(combined)
                    marked.update([a, b])
    return new_groups, marked


def quine_mccluskey(minterms):
    """Prime Implicant を列挙するメイン手続き"""
    groups = initial_grouping(minterms)
    prime_implicants = set()

    while groups:
        new_groups, marked = combine_groups(groups)
        
        for group in groups.values():
            for term in group:
                if term not in marked:
                    prime_implicants.add(term)
        
        groups = new_groups

    return sorted(prime_implicants)


def petricks_method(minterms, implicants):
    """Petrickの方法で最小カバーの組み合わせを選出"""
    # 各最小項がカバーされる PI のインデックスを記録
    table = {m: [] for m in minterms}
    for i, imp in enumerate(implicants):
        for m in minterms:
            if all(a == '-' or a == b for a, b in zip(imp, m)):
                table[m].append(i)

    def distribute(a, b):
        """AND×OR の分配によって組み合わせを展開"""
        result = []
        for x in a:
            for y in b:
                merged = sorted(set(x).union([y]))
                if merged not in result:
                    result.append(merged)
        return result

    # 初期化（1つ目の最小項）
    product = [[i] for i in table[minterms[0]]]
    for m in minterms[1:]:
        product = distribute(product, table[m])

    # 最小項数を持つものを選択
    min_len = min(len(p) for p in product)
    best = [p for p in product if len(p) == min_len][0]
    return [implicants[i] for i in best]


# 7セグメントの真理値表

lookup_table = {
    "0000": [1, 1, 1, 1, 1, 1, 0],
    "0001": [0, 1, 1, 0, 0, 0, 0],
    "0010": [1, 1, 0, 1, 1, 0, 1],
    "0011": [1, 1, 1, 1, 0, 0, 1],
    "0100": [0, 1, 1, 0, 0, 1, 1],
    "0101": [1, 0, 1, 1, 0, 1, 1],
    "0110": [1, 0, 1, 1, 1, 1, 1],
    "0111": [1, 1, 1, 0, 0, 1, 0],
    "1000": [1, 1, 1, 1, 1, 1, 1],
    "1001": [1, 1, 1, 1, 0, 1, 1],
    "1010": [1, 1, 1, 0, 1, 1, 1],
    "1011": [0, 0, 1, 1, 1, 1, 1],
    "1100": [1, 0, 0, 1, 1, 1, 0],
    "1101": [0, 1, 1, 1, 1, 0, 1],
    "1110": [1, 0, 0, 1, 1, 1, 1],
    "1111": [1, 0, 0, 0, 1, 1, 1],
}


# 各セグメントごとに最小項を抽出し、SOPを導出
# ハイフンは don't care、0、1はそれぞれ負と正
if __name__ == "__main__":
    for i in range(7):
        seg = chr(ord('a') + i)
        minterms = [bits for bits, vals in lookup_table.items() if vals[i] == 1]
        implicants = quine_mccluskey(minterms)
        minimized = petricks_method(minterms, implicants)
        print(f"Segment {seg} minimized SOP:")
        for m in minimized:
            print("  ", m)
        print()
