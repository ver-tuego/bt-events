import json

keyboard = {
"one_time" : False,
"buttons" : [
[ {"action" : {
"type" : "text",
"label" : "Включить уведомления"},
"color" : "positive"
}
], [{"action" : {
"type" : "text",
"label" : "Статистика"},
"color" : "primary"
}
]]}

keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

keyboard2 = {
"one_time" : False,
"buttons" : [
[ {"action" : {
"type" : "text",
"label" : "Выключить уведомления"},
"color" : "negative"
}
], [{"action" : {
"type" : "text",
"label" : "Статистика"},
"color" : "primary"
}
]]}

keyboard2 = json.dumps(keyboard2, ensure_ascii = False).encode('utf-8')
keyboard2 = str(keyboard2.decode('utf-8'))
