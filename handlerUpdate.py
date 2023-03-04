# Обработчик обновления

import time
import requests
from config import main_token
from threading import Thread
from methods import actionDB, sender, getTester

class HandlerToken:

    def __init__(self):
        self.iftoken = False
        self.token = ""

def cmd():

    HandlerToken()

    while True:
        if HandlerToken.iftoken == False:


        resultData = actionDB.getAllUsers()
        th = Thread(target=sendTesters, args=(resultData,))
        th.start()
        time.sleep(60)

def sendTesters(resultData):
    for testerId in resultData:
        testerInfo = getTester.cmd(testerId)
        resData = actionDB.checkData(testerId)

        if testerInfo == None:
            pass
        else:
            testerPoint = testerInfo[0].split()

            try:
                testerPoint = int(testerPoint[0]+testerPoint[1])
            except:
                testerPoint = int(testerPoint[0])

            notificationData = actionDB.updateUser(testerId, resData, testerPoint)
            if notificationData == None:
                pass
            else:
                actionDB.dischargeUser(testerId, resData, notificationData[1], notificationData[2])
                if resData[4] != 0:
                    sender.cmd(testerId, (f'{notificationData[0]}\nТекущее количество очков: {testerPoint} \n Позиция в топе: {testerInfo[1]}'), None, None, None)

                chats = actionDB.getChatsNotification(testerId)
                for chat in chats:
                    sent = requests.get('https://api.vk.com/method/users.get', params = {'access_token': main_token, 'v': 5.131, 'user_ids': testerId}).json()['response'][0]
                    sender.cmd(chat[0], (f'[id{testerId}|{sent["first_name"]} {sent["last_name"]}],\n{notificationData[0]}\nТекущее количество очков: {testerPoint} \n Позиция в топе: {testerInfo[1]}'), None, None, None, 1)

        time.sleep(3)
