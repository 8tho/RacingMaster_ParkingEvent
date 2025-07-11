# 車種の定義（７．１２）
vehicles = {
    '毎日新聞社': {'space': 10, 'max_count': 1, 'revenue': 1602, 'label': 'デイリーグループ', 'sb': 0},
    'レガシー4C': {'space': 6, 'max_count': 1, 'revenue': 3240, 'label': 'A', 'sb': 12},
    'レガシージュリア': {'space': 4, 'max_count': 1, 'revenue': 1800, 'label': 'B', 'sb': 12, 'sb_conditions': ['レガシーハチロク']},
    '911カレラ': {'space': 3, 'max_count': 1, 'revenue': 1215, 'label': 'B', 'sb': 10, 'sb_conditions': ['レガシーFIAT', 'レジェFIAT']},
    'レガシーハチロク': {'space': 2, 'max_count': 3, 'revenue': 720, 'label': 'ハチロクグループ', 'sb': 8},
    'レガシーFIAT': {'space': 1, 'max_count': 3, 'revenue': 270, 'label': 'FIATグループ', 'sb': 22},
    'HuayraBC': {'space': 9, 'max_count': 1, 'revenue': 1330, 'label': 'B', 'sb': 25, 'sb_conditions': ['AgeraRS']},
    'レヴェントン': {'space': 9, 'max_count': 2, 'revenue': 1330, 'label': 'B', 'sb': 26, 'sb_conditions': ['Cento']},
    'Cento': {'space': 9, 'max_count': 1, 'revenue': 1330, 'label': 'B', 'sb': 26, 'sb_conditions': ['レヴェントン']},
    '918スパイダー': {'space': 7, 'max_count': 1, 'revenue': 944, 'label': 'A', 'sb': 21},
    'AgeraRS': {'space': 6, 'max_count': 3, 'revenue': 771, 'label': 'A', 'sb': 19},
    'GR86': {'space': 5, 'max_count': 1, 'revenue': 610, 'label': 'B', 'sb': 18, 'sb_conditions': ['R34']},
    'レジェ4C': {'space': 5, 'max_count': 1, 'revenue': 610, 'label': 'A', 'sb': 17},
    'レジェジュリア': {'space': 4, 'max_count': 2, 'revenue': 462, 'label': 'B', 'sb': 14, 'sb_conditions': ['レガシーハチロク']},
    'レジェFIAT': {'space': 1, 'max_count': 1, 'revenue': 90, 'label': 'FIATグループ', 'sb': 11}
}

target_space = 42

def calculate_sb_bonus(combination):
    """SB条件を満たす組み合わせのSBボーナスを計算"""
    total_sb = 0
    used_vehicles = [name for name, count in combination.items() if count > 0]

    # ラベルA：車種でSBが有効な数をカウント
    label_a_sb_count = 0

    # 各ラベルごとに使用車種数をカウント
    label_counts = {}
    for vehicle_name, count in combination.items():
        if count > 0:
            label = vehicles[vehicle_name]['label']
            if label not in label_counts:
                label_counts[label] = 0
            label_counts[label] += 1

    for vehicle_name, count in combination.items():
        if count > 0:
            vehicle_info = vehicles[vehicle_name]
            label = vehicle_info['label']
            sb_value = vehicle_info['sb']

            if label == 'A':
                # ラベルAは最大5つまでSB有効
                if label_a_sb_count < 5:
                    total_sb += sb_value
                    label_a_sb_count += 1

            elif label == 'B':
                # ラベルB：SB条件の車種が組み合わせに含まれる場合のみSB有効
                if 'sb_conditions' in vehicle_info:
                    for condition_vehicle in vehicle_info['sb_conditions']:
                        if condition_vehicle in used_vehicles:
                            total_sb += count * sb_value
                            break

            elif 'グループ' in label:
                # ラベル「〇〇グループ」：2台以上の同ラベルが組み合わせに含まれる場合のみSB有効
                label_total_count = sum(combination[v_name] for v_name in vehicles.keys() 
                                      if vehicles[v_name]['label'] == label)
                if label_total_count >= 2:
                    total_sb += count * sb_value  # (台数)*(各車種のSB)

    return total_sb

def calculate_total_revenue(combination):
    """組み合わせの総合収益を計算 (収益 *(SB+100) / 100 * 1.2)"""
    import math
    
    total_revenue = 0

    for vehicle_name, count in combination.items():
        if count > 0:
            total_revenue += vehicles[vehicle_name]['revenue'] * count

    total_sb = calculate_sb_bonus(combination)

    # SBが0でも基本収益は返す（SB=0の場合は100%、つまり基本収益そのまま）
    # さらに20%増収して、小数第一位繰り上げで整数にする
    result = total_revenue * (total_sb + 100) / 100 * 1.2
    return math.ceil(result)

# マス数がちょうどになる組み合わせを生成
valid_combinations = []

# 各車種の使用数の範囲を設定
vehicle_names = list(vehicles.keys())

def generate_combinations(index, current_combination, current_space):
    """再帰的に組み合わせを生成"""
    if index == len(vehicle_names):
        # 全ての車種を検討し終わった場合
        if current_space == target_space:
            valid_combinations.append(current_combination.copy())
        return

    vehicle_name = vehicle_names[index]
    max_count = vehicles[vehicle_name]['max_count']
    space_per_vehicle = vehicles[vehicle_name]['space']

    # この車種を0台から最大台数まで使用する場合を試す
    for count in range(max_count + 1):
        additional_space = count * space_per_vehicle
        if current_space + additional_space <= target_space:
            current_combination[vehicle_name] = count
            generate_combinations(index + 1, current_combination, current_space + additional_space)
            # バックトラック用にリセット
            current_combination[vehicle_name] = 0

# 組み合わせ生成を開始
generate_combinations(0, {name: 0 for name in vehicle_names}, 0)

# 各組み合わせの総合収益を計算してソート
combination_total_revenues = []
for combo in valid_combinations:
    total_revenue = calculate_total_revenue(combo)
    combination_total_revenues.append((combo, total_revenue))

# 総合収益の高い順にソート
combination_total_revenues.sort(key=lambda x: x[1], reverse=True)

# 上位の組み合わせを表示
print(f"マス数が{target_space}になる組み合わせ数: {len(valid_combinations)}")
print("\n組み合わせランキング:")
print("=" * 100)

for i, (combo, total_revenue) in enumerate(combination_total_revenues[:100], 1):
    print(f"{i:2d}. ", end="")
    used_vehicles = []
    total_space = 0
    base_revenue = 0

    for vehicle_name in vehicle_names:
        count = combo[vehicle_name]
        if count > 0:
            space = count * vehicles[vehicle_name]['space']
            revenue = count * vehicles[vehicle_name]['revenue']
            total_space += space
            base_revenue += revenue
            used_vehicles.append(f"{vehicle_name}×{count}")

    total_sb = calculate_sb_bonus(combo)

    print(f"{' + '.join(used_vehicles)} = {total_space}マス")
    print(f"    収益: {base_revenue}, SB: {total_sb}%, 総合収益: {total_revenue}")
    print()

# 検証：統計情報
print(f"=== 統計情報 ===")
print(f"有効な組み合わせ数: {len(valid_combinations)}")

if len(combination_total_revenues) > 0:
    print(f"最高総合収益: {combination_total_revenues[0][1]}")
    print(f"最低総合収益: {combination_total_revenues[-1][1]}")
    avg_total_revenue = sum(total_revenue for _, total_revenue in combination_total_revenues) / len(combination_total_revenues)
    print(f"平均総合収益: {avg_total_revenue:.2f}")
