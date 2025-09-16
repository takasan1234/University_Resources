from itertools import product
from docplex.mp.model import Model

# 正しい真理値表（各入力に対する7セグメント表示の a〜g の出力値）
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

# 出力 a〜g の各ビットについて個別の真理値表を作成
n = 4  # 入力ビット数
seg_lookup_tables = [{} for _ in range(7)]
for bits, seg_values in lookup_table.items():
    key = int(bits, 2)  # 入力を10進数に変換
    for i, v in enumerate(seg_values):
        seg_lookup_tables[i][key] = v  # 各セグメントごとの真理値表に格納

# すべての論理項（cube）を生成（少なくとも1つはdon't care）
def all_cubes(n):
    for mask in product([-1, 0, 1], repeat=n):
        if all(m != -1 for m in mask):  # 全ビットが確定している場合（完全一致）はスキップ
            continue
        yield mask

# cubeが指定した入力bitsをカバーするかどうかを判定
def covers(cube, bits):
    return all(c == -1 or c == b for c, b in zip(cube, bits))

# 各セグメント（a〜g）について最小SOP（主加法標準形）を探索
for i, table in enumerate(seg_lookup_tables):
    seg_name = chr(ord("a") + i)
    minterms_1 = [k for k, v in table.items() if v == 1]  # 出力が1の入力集合
    minterms_0 = [k for k, v in table.items() if v == 0]  # 出力が0の入力集合
    minterm_bits_1 = [list(map(int, f"{x:04b}")) for x in minterms_1]  # 2進数のビット列に変換
    minterm_bits_0 = [list(map(int, f"{x:04b}")) for x in minterms_0]
    cube_list = list(all_cubes(n))  # 論理項の候補を生成

    mdl = Model(name=f"sop_{seg_name}")  # CPLEXモデル生成
    x = {i: mdl.binary_var(name=f"x_{i}") for i in range(len(cube_list))}  # 各cubeが選ばれるかの変数

    # 出力1をカバーするcubeが必ず1つ以上含まれるよう制約を追加
    for bits in minterm_bits_1:
        mdl.add_constraint(mdl.sum(x[i] for i, cube in enumerate(cube_list) if covers(cube, bits)) >= 1)

    # 出力0をカバーするcubeは使用不可（排他制約）
    for bits in minterm_bits_0:
        for i, cube in enumerate(cube_list):
            if covers(cube, bits):
                mdl.add_constraint(x[i] == 0)

    # 使うcubeの数を最小化（目的関数）
    mdl.minimize(mdl.sum(x[i] for i in x))
    solution = mdl.solve()

    # 解の表示
    # ハイフンは don't care、0、1はそれぞれ負と正
    print(f"Segment {seg_name} minimal SOP:")
    if solution:
        for i, cube in enumerate(cube_list):
            if x[i].solution_value > 0.5:
                expr = "".join(str(b) if b != -1 else "-" for b in cube)
                print("  ", expr)
    else:
        print("  No solution")
    print()
