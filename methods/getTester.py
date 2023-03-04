# Информация о пользователе в программе тестирования

import requests

def cmd(user_id):
        tester_info = requests.get(f"https://ssapi.ru/vk-bugs-api/?method=getReporter&reporter_id={user_id}").json()
        print(tester_info)
        tester_status = tester_info['response']['reporter']['tester']
        if tester_status == False:
            tester_info = None
        else:
            tester_info = [tester_info['response']['reporter']['status_text'], tester_info['response']['reporter']['top_position']]
        return tester_info

