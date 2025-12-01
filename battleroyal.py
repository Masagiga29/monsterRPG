from flask import Flask, render_template, request, session, redirect, url_for
from monster3 import monster_generate, monster_odds, battle_log, check_winner, payout
import ast, copy
app = Flask(__name__)


monster_name = {"メークインアヤカ", "不埒者サクナ", "美人局ミズキ", "ハイスペックハルカ", "ロマンチストルカ"}


@app.route("/")
def index():
  monsters = monster_generate()
  odds = monster_odds()
  for name, stats in monsters.items():
     if name in odds:
      stats["odds"] = odds[name]


  return render_template("battleroyal.html", monsters = monsters)


@app.route("/log")
def battle_log_turn():

# 必要な情報がセッションにあるか確認します
    if 'monsters_current_state' not in session or 'turn_count' not in session:
        # バトルが開始されていないのにアクセスされた場合
        print("エラー: セッションにバトルデータがありません。")
        return redirect(url_for('index'))

    # セッションから現在の状態を読み込みます
    current_state = session['monsters_current_state']
    turn = session['turn_count']

    # --- 1. 勝者判定 (ターン実行「前」にチェック) ---
    # (前のターンで勝者が決まっている可能性があるため)
    winner = check_winner(current_state)

    if winner:
        # 勝者が決まっている場合
        
        # 賭け情報をセッションから取得
        bet_monster = session.get('bet_monster', '不明')
        kakekin = session.get('kakekin', '0')
        initial_state = session.get('monsters_initial_state', {})
        
        try:
            # 賭けたモンスターのオッズを「初期状態」から取得
            bet_odds = initial_state[bet_monster]['odds']
        except KeyError:
            bet_odds = 1.0 # 予期せぬエラーの場合
        
        # 払い戻し計算
        payout_amount, message = payout(winner, kakekin, bet_odds, bet_monster)
        
        # バトル関連のセッションをクリアします (任意)
        session.pop('monsters_current_state', None)
        session.pop('turn_count', None)
        session.pop('battle_log_history', None)
        session.pop('bet_monster', None)
        session.pop('kakekin', None)
        # session.pop('monsters_initial_state', None) # (これは残してもよい)

        # 結果ページ (senntaku.html) をレンダリングします
        return render_template(
            "senntaku.html", 
            article = winner,    # 勝者名
            message = message      # 払い戻しメッセージ
        )
    
    # 1ターン進めます
    (log_this_turn, new_state) = battle_log(current_state)
    
    # セッションを更新します
    session['monsters_current_state'] = new_state
    session['turn_count'] = turn + 1
    
    # (オプション: 全ログを保存する場合)
    if 'battle_log_history' in session:
        session['battle_log_history'].extend(log_this_turn)
        # セッションが大きくなりすぎないよう注意


    return render_template("battlelog.html", turn=turn, current_state=current_state, battle_log=battle_log,turn_log = log_this_turn)


@app.route("/senntaku", methods=["POST"])
def result():
    name = request.form["name"]
    kakekin = request.form["kakekinn"]
    monsters = ast.literal_eval(request.form["monsters"])
    message = f"{name} のオッズは {monsters[name]['odds']} 倍です！"
    article = battle_log(monsters)
   
    payout_amount = payout(article[0], kakekin, monsters[name]['odds'],name)
    if payout_amount > 0:
        message += f"的中！ 払い戻しは {payout_amount} コインです！"
    else:
        message += "残念！ はずれです。"
        



    return render_template("senntaku.html", message = message, article = article[0], name = name,battle = battle_log, kakekin = kakekin, payout_amount = payout_amount)


