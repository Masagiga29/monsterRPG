import random

# --- グローバル変数の定義 (変更なし) ---
monster_name = {"メークインアヤカ", "不埒者サクナ", "美人局ミズキ", "ハイスペックハルカ", "ロマンチストルカ"}
status_key = {"HP", "MP", "ATK", "DEF", "SPD", "MAG"}

monsters = {}  # モンスターのステータスを格納する辞書

# --- 既存の関数 (一部修正) ---

def monster_generate():
    """
    モンスターのステータスをランダムに生成します。
    (Web用に print() を削除)
    """
    global monsters
    monsters = {} 
    
    for name in monster_name:
        status = {value: random.randint(10, 50) for value in status_key}
        status["HP"] = random.randint(50, 100)
        status["Lv"] = int(sum(status.values()) / 10)
        monsters[name] = status
    
    # print文の代わりに、生成情報をリストとして返す
    generated_info = ["--- モンスター生成完了 ---"]
    for key, value in monsters.items():
        generated_info.append(f"{key}: {value}")
    generated_info.append("-" * 20)
    
    return generated_info

# (damage_cal, critical_int, avoiding_rate は変更なし)
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
    return max(0, damage)

def critical_int(attacker):   
    crt = (int(monsters[attacker]["ATK"])) * (random.randint(55, 66)) // 64
    if crt >= 254:
        crt = 254
    return crt

def avoiding_rate(defender):   
    rate = int(monsters[defender]["SPD"]) 
    random_chance = random.randint(1, 100)
    return rate >= random_chance

# --- バトルロイヤル関数 (Web用に大改修) ---

def battle_royale():
    """
    バトルロイヤルを実行し、戦闘ログを「リスト」として返します。
    """
    
    # ログを溜め込むためのリスト
    logs = []
    
    alive_monsters = list(monsters.keys()) 
    
    logs.append("👑👑👑 バトルロイヤル開始！ 👑👑👑")
    
    turn = 1
    while len(alive_monsters) > 1:
        logs.append(f"\n--- ターン {turn} ---")
        logs.append(f"現在の生存者: {', '.join(alive_monsters)} ({len(alive_monsters)}体)")
        
        attacker = random.choice(alive_monsters)
        defenders = [m for m in alive_monsters if m != attacker]
        
        logs.append(f"💥 今ターンの攻撃者: {attacker}")

        for defender in defenders:
            if monsters[defender]["HP"] <= 0:
                continue 

            logs.append(f"\n  {attacker} の {defender} への攻撃！")
            
            if avoiding_rate(defender):
                logs.append(f"  {defender} は攻撃を回避した！ (残りHP: {monsters[defender]['HP']})")
                continue 

            damage = damage_cal(attacker, defender)
            
            crt_rate = critical_int(attacker)
            if random.randint(0, 255) < crt_rate:
                logs.append("  ✨ クリティカルヒット！ ✨")
                damage = int(damage * 1.5)
            
            monsters[defender]["HP"] -= damage
            
            if monsters[defender]["HP"] <= 0:
                monsters[defender]["HP"] = 0
                logs.append(f"  {defender} は {damage} のダメージを受けた。")
                logs.append(f"  💀 {defender} は倒れた！ 💀")
            else:
                logs.append(f"  {defender} は {damage} のダメージを受けた。 (残りHP: {monsters[defender]['HP']})")
        
        alive_monsters = [m for m in alive_monsters if monsters[m]["HP"] > 0]
        
        turn += 1
        if turn > 100:
            logs.append("100ターン経過したため、強制終了します。")
            break

    if len(alive_monsters) == 1:
        logs.append(f"\n\n--- 🏆 バトル終了 🏆 ---")
        logs.append(f"最後の生き残りは {alive_monsters[0]} です！ おめでとう！")
    else:
        logs.append("\n\n--- バトル終了 ---")
        logs.append("勝者は決まりませんでした。")

    # 最後に、溜め込んだログのリストを返す
    return logs