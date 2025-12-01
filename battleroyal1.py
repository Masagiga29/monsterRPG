from flask import Flask, render_template, request, session, redirect, url_for
from monster3 import monster_generate, monster_odds, battle_log, check_winner, payout
import ast, copy
app = Flask(__name__)


app.secret_key = 'your_very_secret_key_here' 


@app.route("/", methods=["GET"])
def index():
  monsters = monster_generate()
  
  # --- 修正: monster_odds に monsters を渡す ---
  monsters_with_odds = monster_odds(monsters)
  
  # モンスター情報をセッションに一時的に保存 (POSTで参照するため)
  session['initial_monsters_for_betting'] = monsters_with_odds

  return render_template("battleroyal.html", monsters = monsters_with_odds)

@app.route("/", methods=["POST"])
def start_battle():
    
    bet_monster = request.form.get("name")
    kakekin = request.form.get("kakekinn") 
    monsters_str = request.form["monsters"]
    initial_monsters = ast.literal_eval(monsters_str)
    

    # --- バトル情報をセッションに保存 ---
    session['bet_monster'] = bet_monster
    session['kakekin'] = kakekin
    session['monsters_initial_state'] = initial_monsters 
    session['monsters_current_state'] = copy.deepcopy(initial_monsters) 
    session['turn_count'] = 1
    session['battle_log_history'] = [] # ログ履歴を初期化

    # --- バトルログページへリダイレクト ---
    return redirect(url_for('battle_log_turn'))


@app.route("/log")
def battle_log_turn():

    
    current_state = session['monsters_current_state']
    turn = session['turn_count']


    winner = check_winner(current_state)

    if winner:
        # 勝者が決まっている場合
        
        bet_monster = session.get('bet_monster', '不明')
        kakekin = session.get('kakekin', '0')
        initial_state = session.get('monsters_initial_state', {})
        
        try:
            # 賭けたモンスターのオッズを「初期状態」から取得
            bet_odds = initial_state[bet_monster]['odds']
        except KeyError:
            bet_odds = 1.0 # 予期せぬエラーの場合
        
        # --- 修正: 修正した payout 関数を呼び出す ---
        (payout_amount, message) = payout(winner, kakekin, bet_odds, bet_monster)
        

        return render_template("senntaku.html", article = winner, message = message, payout_amount = payout_amount)
    
    # --- 2. 勝者がまだいない場合: 1ターン進める ---
    (log_this_turn, new_state) = battle_log(current_state)
    
    # セッションを更新します
    session['monsters_current_state'] = new_state
    session['turn_count'] = turn + 1

    return render_template("battlelog.html",turn=turn,current_state=new_state,turn_log = log_this_turn)
