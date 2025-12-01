import random
import copy # モンスターの状態を安全にコピーするために必要

# モンスター名とステータスキーを定数として定義
MONSTER_NAME = {"メークインアヤカ", "不埒者サクナ", "美人局ミズキ", "ハイスペックハルカ", "ロマンチストルカ"}
STATUS_KEY = {"HP", "MP", "ATK", "DEF", "SPD", "MAG"}

def monster_generate():
    """
    モンスターの初期ステータス辞書を生成して返します。
    """
    monsters = {} # ローカル変数として定義
    for name in MONSTER_NAME:
        status = {value: random.randint(10, 50) for value in STATUS_KEY}
        status["Lv"] = int(sum(status.values()) / 10)
        # バトルのために最大HPを記録しておくと便利ですが、今回はHPのみ使います
        # status["MAX_HP"] = status["HP"] 
        monsters[name] = status
    return monsters

def monster_odds(monsters):
    """
    モンスターの辞書を受け取り、オッズを計算して「追加」した辞書を返します。
    """
    
    # 元の辞書を変更しないようにディープコピー
    monsters_with_odds = copy.deepcopy(monsters)

    sorted_monsters = sorted(monsters.items(), key = lambda item: item[1]["Lv"])

    base_odds = [2.0, 3.0, 4.0, 5.0, 6.0]
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
        odds_to_assign = base_odds[current_odds_index : current_odds_index + num_monsters_in_level]

        if not odds_to_assign:
            break

        if num_monsters_in_level > 1:
            average_odds = sum(odds_to_assign) / len(odds_to_assign)
            # オッズを小数点以下1桁に丸める
            avg_odds_rounded = round(average_odds, 1)
            for name in names_in_level:
                assigned_odds[name] = avg_odds_rounded
        else:
            assigned_odds[names_in_level[0]] = odds_to_assign[0]
        current_odds_index += num_monsters_in_level
    
    # オッズを monsters_with_odds 辞書に追加
    for name, stats in monsters_with_odds.items():
        if name in assigned_odds:
            stats["odds"] = assigned_odds[name]
        else:
            # オッズが割り当てられなかった場合のデフォルト値
            stats["odds"] = 99.9 

    return monsters_with_odds

# --- 戦闘計算関数群 (引数を受け取るように修正) ---

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

def avoiding_rate(defender_stats):
    rate = int(defender_stats["SPD"]) 
    random_chance = random.randint(1, 100)
    return rate >= random_chance # True / False を返す

# --- 新しいバトルロジック ---

def battle_turn(monsters_state):
    """
    現在のモンスター状態 (辞書) を受け取り、
    1ターン分のバトルを実行し、
    (ログのリスト, 更新されたモンスター状態) を返します。
    """
    
    # 元の状態を変更しないようにディープコピーします
    current_monsters = copy.deepcopy(monsters_state)
    turn_log = [] # このターンのログ

    # 生き残っているモンスターをリストアップ
    alive_monsters = [name for name, stats in current_monsters.items() if stats["HP"] > 0]
    
    # 勝者がすでに決まっているか、バトルが不可能な場合は即座に返します
    if len(alive_monsters) <= 1:
        return (["バトルは既に終了しています。"], current_monsters)

    # 攻撃者をランダムに選択
    attacker_name = random.choice(alive_monsters)
    attacker_stats = current_monsters[attacker_name]
    
    # 防御者（攻撃者以外）をランダムに選択
    defenders = [m for m in alive_monsters if m != attacker_name]
    if not defenders:
         return (["攻撃対象がいません。"], current_monsters)
         
    defender_name = random.choice(defenders)
    defender_stats = current_monsters[defender_name]

    log_entry = f"{attacker_name} の攻撃！ -> {defender_name}"

    # 回避判定
    if avoiding_rate(defender_stats):
        log_entry += " ...しかし、攻撃は回避された！"
        turn_log.append(log_entry)
        # 状態は変更せずログを返します
        return (turn_log, current_monsters) 

    # ダメージ計算
    damage = damage_cal(attacker_stats, defender_stats)
        
    # クリティカル判定
    crt_rate = critical_int(attacker_stats)
    if random.randint(0, 255) < crt_rate:
        log_entry += " ...痛恨の一撃！"
        damage = int(damage * 1.5)
    
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
    """
    モンスターの状態を受け取り、勝者がいればその名前 (str) を、
    いなければ None を返します。
    """
    alive_monsters = [name for name, stats in monsters_state.items() if stats["HP"] > 0]
    
    if len(alive_monsters) == 1:
        return alive_monsters[0] # 勝者の名前を返す
    else:
        return None # まだ勝者はいない


def payout(winner_name, kakekin_str, bet_odds, bet_monster_name):
    """
    勝者、賭け金（文字列）、オッズ、賭けたモンスターに基づいて
    払い戻し金額と結果メッセージを計算して返します。
    (この関数はバトルを実行しません)
    """
    
    try:
        # 賭け金を整数に変換
        kakekin_int = int(kakekin_str)
        if kakekin_int < 0:
            kakekin_int = 0
    except (ValueError, TypeError):
        kakekin_int = 0 # 賭け金が無効な場合は0とする

    payout_amount = 0
    
    if winner_name == bet_monster_name:
        # 賭けが的中した場合
        payout_amount = kakekin_int * bet_odds
        # 小数点以下を切り捨て
        payout_amount = int(payout_amount) 
        
        message = f"的中！ {winner_name} が勝利しました。"
        message += f" 賭け金: {kakekin_int} コイン (オッズ: {bet_odds} 倍)"
        message += f" 払い戻し: {payout_amount} コイン"
    else:
        # 賭けが外れた場合
        message = f"残念...あなたが賭けた {bet_monster_name} は負けました。(勝者は {winner_name} です)"
        message += f" 賭け金 {kakekin_int} コインは失われました。"

    # 払い戻し金額とメッセージの両方を返す
    return payout_amount, message

# --- ファイル末尾の関数呼び出しは削除します ---
# (Flaskアプリから呼び出すため、import時に実行する必要はありません)

print(monster_generate())
print(monster_odds())


# ...