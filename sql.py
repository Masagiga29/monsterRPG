import pymysql

print("Connecting to database...")

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='masa1009',
    db='paiza',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

sql = "SELECT * FROM users "
cursor = connection.cursor()
cursor.execute(sql)
players = cursor.fetchall()

cursor.close()
connection.close()

for player in players:
  print(player["id"])

