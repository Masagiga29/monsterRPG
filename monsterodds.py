




def monster_odds(monsters):
   
    
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
            for name in names_in_level:
                assigned_odds[name] = average_odds
        else:
            assigned_odds[names_in_level[0]] = odds_to_assign[0]
        current_odds_index += num_monsters_in_level

    return assigned_odds
