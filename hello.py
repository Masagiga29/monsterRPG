from flask import Flask, render_template
app = Flask(__name__)
import pymysql

def getConnection():
    return pymysql.connect(
        host='localhost',
        db='paiza',
        user='root',
        password='masa1009',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route('/')
def select_sql():
  
    connection = getConnection()
    message = "Hello world"
    cursor = connection.cursor()
    sql = "insert into players (name, level, job_id) values ('霧島１' , 1,1)" 
    cursor.execute(sql)
    connection.commit()
    sql = "SELECT * FROM players"
    cursor.execute(sql)
    players = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view.html', message = message, players = players)




@app.route("/about")
def about():
    return render_template("index.html")