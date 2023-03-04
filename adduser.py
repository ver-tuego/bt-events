import sqlite3 as sql
con = sql.connect('data/allUsers.db', check_same_thread = False)
cur = con.cursor()

user_id = int(input('айди юзера: '))
point = int(input('количество очков: '))

cur = con.cursor()
cur.execute(f"INSERT INTO `allUsers` VALUES (?, ?, ?, ?, ?)", (user_id, point, '', 0, 0,))
con.commit(); cur.close()
