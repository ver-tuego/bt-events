import vk_api
import requests
import time
import re
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread
from keyboards import keyboard, keyboard2
from config import main_token
import handlerUpdate
from methods import sender, getTester, actionDB, getStat

tokenApiVk = vk_api.VkApi(token = main_token)
vk_session = tokenApiVk.get_api()
longpoll = VkLongPoll(tokenApiVk) # Авторизация токена.

th = Thread(target=handlerUpdate.cmd, args=())
th.start()

def main():
    for event in longpoll.listen(): # Обработчик для личных сообщений бота.
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                message_text = event.text.lower()
                user_id = event.user_id

                if message_text in ['включить уведомления', 'включить', 'вкл']:
                    testerInfo = getTester.cmd(user_id)
                    resultData = actionDB.checkData(user_id)
                    if testerInfo == None:
                        sender.cmd(user_id, 'Вы не состоите в программе тестирования.')
                    else:
                        if len(resultData) == 0:
                            testerInfo = testerInfo[0].split()
                            try:
                                testerInfo = int(testerInfo[0]+testerInfo[1])
                            except:
                                testerInfo = int(testerInfo[0])
                            actionDB.addUser(user_id, testerInfo, 1)
                            sender.cmd(user_id, 'Вы подписались на уведомления о ежедневном обновлении рейтинга.', keyboy = keyboard2)
                        elif resultData[4] == 1:
                            sender.cmd(user_id, 'У Вас уже включены уведомления.', keyboy = keyboard2)
                        else:
                            actionDB.updateNotification(user_id, 1)
                            sender.cmd(user_id, 'Вы подписались на уведомления о ежедневном обновлении рейтинга.', keyboy = keyboard2)

                elif message_text in ['выключить уведомления', 'выключить', 'выкл']:
                    testerInfo = getTester.cmd(user_id)
                    resultData = actionDB.checkData(user_id)
                    if testerInfo == None:
                        sender.cmd(user_id, 'Вы не состоите в программе тестирования.')
                    else:
                        if len(resultData) == 0:
                            sender.cmd(user_id, 'У Вас уже выключены уведомления.', keyboy = keyboard)
                        elif resultData[4] == 0:
                            sender.cmd(user_id, 'У Вас уже выключены уведомления.', keyboy = keyboard)
                        else:
                            actionDB.updateNotification(user_id, 0)
                            sender.cmd(user_id, 'Вы отписались от уведомлений о ежедневном обновлении рейтинга.', keyboy = keyboard)
                elif message_text in ['стата', 'статистика']:
                    testerInfo = getTester.cmd(user_id)
                    resultData = actionDB.checkData(user_id)
                    if testerInfo == None:
                        sender.cmd(user_id, 'Вы не состоите в программе тестирования.')
                    else:
                        try:
                            if len(resultData) == 0:
                                sender.cmd(user_id, 'Невозможно получить статистику, похоже вы не подписаны на уведомления', keyboy = keyboard)
                            elif resultData[3] == 0:
                                sender.cmd(user_id, 'Подсчёт недельной статистики только начался, ждите обновления рейтинга.')
                            else:
                                getStat.cmd(resultData[2], resultData[1], resultData[3])
                                getUrl = tokenApiVk.method("photos.getMessagesUploadServer")
                                server = requests.post(getUrl['upload_url'], files = {'photo': open('result.png', 'rb')}).json()
                                uploadImage = tokenApiVk.method('photos.saveMessagesPhoto', {'photo':server['photo'], 'server': server['server'], 'hash': server['hash']})[0]
                                resultImage = f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}'

                                resultPoint = re.sub(r"_", " ", resultData[2]).split()
                                num = [len(resultPoint) - 1, 0, 0]; result = ''
                                while num[0] != -1:
                                    result += (f"{resultPoint[num[0]]} рейтинга {num[2]} дн. назад\n")
                                    num = [num[0] - 1, num[1] + int(resultPoint[num[0]]), num[2] + 1]

                                resultPoint = (f'Твоя статистика рейтинга за {resultData[3]} дн.\n {result}\nИтоговый прогресс: {num[1]}')
                                sender.cmd(user_id, resultPoint, atach = resultImage)
                        except ValueError:
                            sender.cmd(user_id, 'Вы не подписаны на уведомления, чтоб получить информацию о еженедельном рейтинге')

def handlerExcept():
    if __name__ == '__main__':
        try:
            main()
        except requests.exceptions.ConnectionError:
            time.sleep(2)
            handlerExcept()
        except requests.exceptions.ReadTimeout:
            time.sleep(2)
            handlerExcept()

if __name__ == '__main__':
    handlerExcept()
