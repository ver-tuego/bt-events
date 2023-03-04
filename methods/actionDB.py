import sqlite3 as sql

con = sql.connect('data/allUsers.db', check_same_thread = False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS `allUsers` (`id` INT, `point` INT, `pointWeek` STRING, `days` INT, `notification` INT)")
cur.execute("CREATE TABLE IF NOT EXISTS `chatNotification` (`chat_id` INT, `user` INT, `off` INT)")
con.commit(); cur.close()

def declOfNum(number, words):
    return words[2 if number % 100 > 4 and number % 100 < 20 else [2, 0, 1, 1, 1, 2][number % 10 < 5 if number % 10 else 5]]

def addUser(user_id, point, notification):
    cur = con.cursor()
    cur.execute(f"INSERT INTO `allUsers` VALUES (?, ?, ?, ?, ?)", (user_id, point, '', 0, notification,))
    con.commit(); cur.close()

def checkData(user_id): # Статистика
    cur = con.cursor()
    cur.execute("SELECT * FROM `allUsers` WHERE id = ?", (user_id,))
    result = cur.fetchall()
    con.commit(); cur.close()
    if len(result) != 0:
        return result[0]
    else:
        return result

def updateNotification(user_id, notification):
    cur = con.cursor()
    cur.execute(
                'UPDATE allUsers SET notification = ? WHERE id = ?', (notification, user_id))
    con.commit(); cur.close()

def updateUser(user_id, data, point):
    cur = con.cursor()
    if data[1] > point:
        resultUpdate = [f'Привет. Ты потерял {data[1] - point} очков рейтинга!', 2, data[1] - point]
    elif data[1] < point:
        resultUpdate = [f'Привет. Ты получил {point - data[1]} очков рейтинга', 1, point - data[1]]
    else:
        resultUpdate = None
    cur.execute(
                'UPDATE allUsers SET point = ? WHERE id = ?', (point, user_id))
    con.commit(); cur.close()
    return resultUpdate

def dischargeUser(user_id, data, step, point):
    cur = con.cursor()
    if data[3] >= 14:
        cur.execute(
                    'UPDATE allUsers SET pointWeek = ?, days = ? WHERE id = ?', ('', 0, user_id))
    if step == 1:
        point = ('+' + str(point) + '_')
        cur.execute(
                    'UPDATE allUsers SET pointWeek = ?, days = ? WHERE id = ?', (str(data[2]) + point, data[3] + 1, user_id))
    elif step == 2:
        point = ('-' + str(point) + '_')
        cur.execute(
                    'UPDATE allUsers SET pointWeek = ?, days = ? WHERE id = ?', (str(data[2]) + point, data[3] + 1, user_id))
    con.commit(); cur.close()

def addChatUser(chat, user):
    cur = con.cursor()
    cur.execute('INSERT INTO `chatNotification` VALUES (?, ?, ?)', (chat, user, 0,))
    con.commit(); cur.close()

def removeChatUser(chat, user):
    cur = con.cursor()
    cur.execute('DELETE FROM `chatNotification` WHERE chat_id = ? and user = ?', (chat, user,))
    con.commit(); cur.close()

def getChatsNotification(user):
    cur = con.cursor()
    cur.execute('SELECT chat_id, off FROM `chatNotification` WHERE user = ?', (user,))
    result = cur.fetchall()
    con.commit(); cur.close()
    return result

def getUserInfo(user):
    cur = con.cursor()
    cur.execute('SELECT * FROM `allUsers` WHERE id = ?', (user,))
    return cur.fetchall()
    con.commit(); cur.close()

def getChatNotification(chat):
    cur = con.cursor()
    cur.execute('SELECT user FROM `chatNotification` WHERE chat_id = ?', (chat,))
    result = cur.fetchall()
    con.commit(); cur.close()
    return result

def getAllUsers():
    cur = con.cursor()
    cur.execute('SELECT id FROM `allUsers`')
    result = cur.fetchall()
    con.commit(); cur.close()
    return [i[0] for i in result]
