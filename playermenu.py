from flask import Flask, render_template
app = Flask(__name__)

player = "勇者"

@app.route("/")
def menu():
  return render_template("menu.html", player_name = player)