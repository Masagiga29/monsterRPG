import random
import copy

monster_name = {"メークインアヤカ", "不埒者サクナ", "美人局ミズキ", "ハイスペックハルカ", "ロマンチストルカ"}
status_key = {"HP", "MP", "ATK", "DEF", "SPD", "MAG"}


def monster_generate():
    monsters = {}
    for name in monster_name:
        status = {value: random.randint(10, 50) for value in status_key}
        status["Lv"] = int(sum(status.values()) / 10)
        monsters[name] = status
    return monsters

def monster_odds(monsters):
    monsters_with_odds = copy.deepcopy(monsters)
    sorted_monsters = sorted(monsters.items(), key = lambda item: item[1]["Lv"])

    base_odds = [6.0, 5.0, 4.0, 3.0, 2.0]
    assigned_odds = {}
    current_odds_index = 0

    levels = {}
    for name, status in sorted_monsters:
        lv = status["Lv"]
        if lv not in levels:
            levels[lv] = []
        levels[lv].append(name)

    for lv in sorted(levels.keys()):
        names_in_level = levels[lv]
        num_monsters_in_level = len(names_in_level)
        
        # オッズが足りなくなる場合
        if current_odds_index >= len(base_odds):
            break 
            
        odds_to_assign = base_odds[current_odds_index : min(current_odds_index + num_monsters_in_level, len(base_odds))]
        
        if not odds_to_assign:
            break

        if num_monsters_in_level > 1 and len(odds_to_assign) > 1:
            average_odds = sum(odds_to_assign) / len(odds_to_assign)
            avg_odds_rounded = round(average_odds, 1)
            for name in names_in_level:
                assigned_odds[name] = avg_odds_rounded
            current_odds_index += len(odds_to_assign)
        
        elif num_monsters_in_level == 1 or (num_monsters_in_level > 1 and len(odds_to_assign) == 1):
             # モンスターが1体、または複数だがオッズが1つしか残っていない場合
            avg_odds_rounded = round(odds_to_assign[0], 1)
            if num_monsters_in_level == 1:
                 assigned_odds[names_in_level[0]] = avg_odds_rounded
            else:
                for name in names_in_level:
                    assigned_odds[name] = avg_odds_rounded
            current_odds_index += 1
            
            
    for name, stats in monsters_with_odds.items():
        if name in assigned_odds:
            stats["odds"] = assigned_odds[name]
        else:
            stats["odds"] = 99.9 

    return monsters_with_odds


# --- 修正: 引数として個々のステータス (辞書) を受け取る ---

def damage_cal(attacker_stats, defender_stats): 
    # グローバルの 'monsters' ではなく、渡された 'stats' 辞書を使う
    atk = int(attacker_stats["ATK"])
    Def = int(defender_stats["DEF"])
    D = (atk - Def / 2) / 2
    damage = 0
    if D <= 2:
        damage += random.randint(0, 1)
    elif 2 <= D < 9:
        damage += random.randint(int(D) - 2, int(D))
    elif 9 <= D:
        damage +=int(( D * 7 )// 8 + ((D/ 4 + 1) * random.randint(0,255)) // 256)
    return damage

def critical_int(attacker_stats):   #critical率を生成。
    # グローバルの 'monsters' ではなく、渡された 'stats' 辞書を使う
    crt = (int(attacker_stats["ATK"])) * (random.randint(55, 66)) // 64
    if crt >= 254:
        crt = 254
    return crt

def avoiding_rate(defender_stats):   #回避率をbool型で出力
    # グローバルの 'monsters' ではなく、渡された 'stats' 辞書を使う
    rate = int(defender_stats["SPD"]) 
    random_chance = random.randint(1, 100)
    if rate >= random_chance:
        return True
    else:
        return False



def damage_cal(attacker_stats, defender_stats): 
    
    atk = int(attacker_stats["ATK"])
    Def = int(defender_stats["DEF"])
    D = (atk - Def / 2) / 2
    damage = 0
    if D <= 2:
        damage += random.randint(0, 1)
    elif 2 <= D < 9:
        damage += random.randint(int(D) - 2, int(D))
    elif 9 <= D:
        damage +=int(( D * 7 )// 8 + ((D/ 4 + 1) * random.randint(0,255)) // 256)
    return damage

def critical_int(attacker_stats):

    crt = (int(attacker_stats["ATK"])) * (random.randint(55, 66)) // 64
    if crt >= 254:
        crt = 254
    return crt

def avoiding_rate(defender_stats):   #回避率をbool型で出力
    # 修正: グローバルの 'monsters' ではなく、渡された 'stats' 辞書を使う
    # (エラーの原因はここの行です)
    rate = int(defender_stats["SPD"]) 
    random_chance = random.randint(1, 100)
    if rate >= random_chance:
        return True
    else:
        return False


def battle_log(monsters_state):
    current_monsters = copy.deepcopy(monsters_state)
    turn_log = []
    
    alive_monsters = [name for name, stats in current_monsters.items() if stats["HP"] > 0]
    attacker_name = random.choice(alive_monsters)
    attacker_stats = current_monsters[attacker_name]
    
    defenders = [m for m in alive_monsters if m != attacker_name]
    defender_name = random.choice(defenders)
    defender_stats = current_monsters[defender_name]
    log_entry = f"{attacker_name} の攻撃！ -> {defender_name}"

    if avoiding_rate(defender_stats):
        log_entry += " ...ひらりと身をかわした！"
        turn_log.append(log_entry)
        return (turn_log, current_monsters) 

    # --- 修正確認: ダメージ計算に 'attacker_stats' と 'defender_stats' を渡す ---
    damage = damage_cal(attacker_stats, defender_stats)
        
    # --- 修正確認: クリティカル判定に 'attacker_stats' を渡す ---
    crt_rate = critical_int(attacker_stats)
    if random.randint(0, 255) < crt_rate:
        log_entry += " ...痛恨の一撃！"
        damage = int(damage * 1.5)
    
    # (以降の battle_log, check_winner, payout, ... は前回の修正のままでOKです)
    
    # ダメージ適用
    defender_stats["HP"] -= damage
    
    if defender_stats["HP"] <= 0:
        defender_stats["HP"] = 0
        log_entry += f" ...{damage} のダメージ。 {defender_name} は倒れた！"
    else:
        log_entry += f" ...{damage} のダメージ。(残りHP: {defender_stats['HP']})"
    
    turn_log.append(log_entry)
    
    # 更新された状態とログを返します
    return (turn_log, current_monsters)


def check_winner(monsters_state):
    alive_monsters = [name for name, stats in monsters_state.items() if stats["HP"] > 0]
    if len(alive_monsters) == 1:
        return alive_monsters[0]
    return None

# --- battle_royale() 関数は /log ルートでは使用しないため、削除またはコメントアウト ---
# (元の /senntaku (POST) での一括実行ロジックで使われていたもの)
# def battle_royale(): ...


# --- 修正: payout 関数 ---
# battle_royale() を呼び出さず、渡された引数に基づいて計算する
def payout(winner, kakekin_str, odds, bet_monster):
    
    # winner は /log ルートから渡された勝者名 (文字列)
    # kakekin はフォームから来た文字列なので数値に変換
    try:
        kakekin = int(kakekin_str)
        if kakekin < 0:
            kakekin = 0
    except (ValueError, TypeError):
        kakekin = 0 # 賭け金が無効な場合は0として扱う

    payout_amount = 0
    message = ""
    
    if winner == bet_monster:
        # オッズ (float) と賭け金 (int) を計算
        payout_amount = int(kakekin * odds)
        message = f"的中！ 払い戻しは {payout_amount} コインです！"
    else:
        message = f"残念！ はずれです。(勝者は {winner} です)"
        # 賭け金は失われる (payout_amount は 0 のまま)
    
    # 払い戻し額とメッセージをタプルで返す
    return (payout_amount, message)

# --- ファイル末尾のグローバルな実行を削除 ---
# (これらは Flask の index ルートで実行されます)