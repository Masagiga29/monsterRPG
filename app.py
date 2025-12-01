from flask import Flask, render_template, jsonify

# ステップ2で作成した battle_logic.py から関数をインポート
import battle_logic

# Flaskアプリの初期化
app = Flask(__name__)

# ルート1: Webページの表示
# http://127.0.0.1:5000/ にアクセスが来たら...
@app.route('/')
def index():
    # ... templates/index.html をブラウザに表示する
    return render_template('index.html')

# ルート2: バトルの実行 (API)
# /start-battle に (JavaScriptから) リクエストが来たら...
@app.route('/start-battle', methods=['POST'])
def start_battle():
    
    # 1. モンスターを（再）生成する (HPをリセットするため)
    generation_logs = battle_logic.monster_generate()
    
    # 2. バトルロイヤルを実行し、ログのリストを受け取る
    battle_logs = battle_logic.battle_royale()
    
    # 3. 生成ログとバトルログを結合する
    all_logs = generation_logs + battle_logs
    
    # 4. ログのリストを JSON 形式で JavaScript に返す
    return jsonify(logs=all_logs)

# メインの実行処理
if __name__ == '__main__':
    # サーバーを起動する (デバッグモードON)
    app.run(debug=True)