import random
import copy

monster_name = {"メークインアヤカ", "不埒者サクナ", "美人局ミズキ", "ハイスペックハルカ", "ロマンチストルカ"}
status_key = {"HP", "MP", "ATK", "DEF", "SPD", "MAG"}

monsters = {} 

def monster_generate():

    for name in monster_name:
        status = {value: random.randint(10, 50) for value in status_key}
        status["Lv"] = int(sum(status.values()) / 10)
        monsters[name] = status

    for key, value in monsters.items():
        print(key, value)

    return monsters


def monster_odds(monsters):
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



   

# def atk_decision():
#     attacker, defender = random.sample(monster_name, 2)
#     return (attacker, defender)
    
    
def damage_cal(attacker,defender): 
    atk = int(monsters[attacker]["ATK"])
    Def = int(monsters[defender]["DEF"])
    D = (atk - Def / 2) / 2
    damage = 0
    if D <= 2:
        damage += random.randint(0, 1)
    elif 2 <= D < 9:
        damage += random.randint(int(D) - 2, int(D))
    elif 9 <= D:
        damage +=int(( D * 7 )// 8 + ((D/ 4 + 1) * random.randint(0,255)) // 256)
    return damage



def critical_int(attacker):   #critical率を生成。
    crt = (int(monsters[attacker]["ATK"])) * (random.randint(55, 66)) // 64
    if crt >= 254:
        crt = 254
    return crt

def avoiding_rate(defender):   #回避率をbool型で出力
    rate = int(monsters[defender]["SPD"]) 
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
    if not defenders:
         return (["攻撃対象がいません。"], current_monsters)
    defender_name = random.choice(defenders)
    defender_stats = current_monsters[defender_name]
    log_entry = f"{attacker_name} の攻撃！ -> {defender_name}"


    if avoiding_rate(defender_stats):
        log_entry += " ...ひらりと身をかわした！"
        turn_log.append(log_entry)
        return (turn_log, current_monsters) 

    
    damage = damage_cal(attacker_stats, defender_stats)
        

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
    alive_monsters = [name for name, stats in monsters_state.items() if stats["HP"] > 0]
    if len(alive_monsters) == 1:
        return alive_monsters[0]
    return None



def battle_royale():
    turn = 1
    alive_monsters = list(monsters.keys())
    while len(alive_monsters) > 1:
        attacker = random.choice(alive_monsters)
        defenders = [m for m in alive_monsters if m != attacker]
        for defender in defenders:
            if monsters[defender]["HP"] <= 0:
                continue 

        if avoiding_rate(defender):
                continue
        damage = damage_cal(attacker, defender)
        crt_rate = critical_int(attacker)

        if random.randint(0, 255) < crt_rate:
            print("痛恨の一撃！")
            damage = int(damage * 1.5)
        monsters[defender]["HP"] -= damage
        
        if monsters[defender]["HP"] <= 0:
            monsters[defender]["HP"] = 0
            print(f"  {defender} は {damage} のダメージを受けた。")
            print(f"     {defender} は倒れた！")
        else:
            print(f"  {defender} は {damage} のダメージを受けた。 (残りHP: {monsters[defender]['HP']})")

        alive_monsters = [m for m in alive_monsters if monsters[m]["HP"] > 0]
        
        
        if len(alive_monsters) == 1:
                
                print(f"\n\n--- バトル終了! ---")
                print(f"最後の生き残りは {alive_monsters[0]} です")
        else:
            turn += 1
            print(f"\n--- ターン {turn} ---")
        

    return alive_monsters


def payout(winner, kakekin, odds_dict, bet_monster):

    winner = battle_royale()
    payout_amount = 0
    
    if winner[0] == bet_monster:
        payout_amount = int(int(kakekin) * odds_dict)
        return payout_amount
    
    else:
        print(f"残念...{bet_monster} は負けました。(勝者は {winner} です)")
        print(f"賭け金 {kakekin} コインは失われました。")
        return 0


monster_generate()
monster_odds()



# for name in monster_name:: monster_name リストからモンスターの名前を一つずつ取り出し、name という変数に代入してループ処理を行う

# status = {key: random.randint(10, 50) for key in status_key}: ループの内部で、元のコードと同じようにして、HPやATKなどの各ステータスにランダムな値を設定した status 辞書を作成します。この処理がループのたびに行われるため、モンスターごとに異なるステータスが生成されます。

# status["Lv"] = int(sum(status.values()) / 10): 計算したステータス合計値からレベルを算出します。

# monsters[name] = status: モンスターの名前 name をキーとして、今作成した status 辞書を monsters 辞書に格納します。


