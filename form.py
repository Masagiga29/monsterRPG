from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def show():
  message = "hello world"
  return render_template("form.html", message = message)

@app.route("/result" , methods= ["GET","POST"])
def result():
  message = "フォームが送信されました"
  if request.method == "POST":
      article1 = request.form["article"]
      name1 = request.form["name"]
  else:
      article1 = request.args.get("article")
      name1 = request.args.get("name")
  return render_template("form.html", message = message, article = article1, name = name1)

