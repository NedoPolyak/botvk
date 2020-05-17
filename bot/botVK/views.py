from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from django.shortcuts import render
import json, vk, random
import sqlite3
import database

session = vk.Session(access_token="dc1b1e7a27edd81f03b53fa59cc37e23c8bd23a506a755630eedbcfbb4d07964476568ed14b7950ee27db")
vkAPI = vk.API(session)

##version - 5.103
@csrf_exempt
def bot(request):
    body  = json.loads(request.body)
    print(body)
    if body == { "type": "confirmation", "group_id": 194135947 }:
        return HttpResponse("61f00e45")
    if body['type'] == "message_new":
        userID = body['object']['message']["from_id"]
        payload = body["object"]["message"]["payload"]
        msg = body['object']['message']["text"]
        answ = ""
        attach = ""
        userInfo = vkAPI.users.get(user_ids = userID, v=5.103)[0]
        if "payload" in body["object"]["message"]:
            payload = body["object"]["message"]["payload"]
            if payload == """{"command":"start"}""":
                keyboardstart(request, userID)
            else:
                try:
                    gpid = -1
                    gpname = ""
                    if payload == """{"command":"admins"}""":
                        gpid = str(1)
                        gpname = "Админ"
                    elif payload == """{"command":"moders"}""":
                        gpid = str(2)
                        gpname = "Модер"
                    elif payload == """{"command":"nothings"}""":
                        gpid = str(3)
                        gpname = "Холоп"
                    database.insert("users", ["id, groupId"], [str(userID), gpid])
                    speak(request,userID, userInfo, answ = "Вы были добавлены в группу {0}".format(gpname))
                except Exception as e:
                    speak(request,userID, userInfo, answ = "Error") 
        else:
            speak(request,userID, userInfo, msg)
        sendAnswer(userID, answ, attach)
def speak(request,userID, userInfo = "", msg = "",  answ = "", attach=""):
    if msg == "/help":
        answ = """Команды:
        /say "cообщение" - возврат вашего сообщения
        /relax - Спасибо, если выберите это
        /wake up - не спасибо, если выберите это после relax"""
    elif msg[:4] == "/say":
        answ = msg[5:]
    if msg[:6] == "/teach":
        pos = msg.find("?")
        newMsg = msg[7:pos].replace(" ", "")
        newAnsw = msg[pos+1:]
        database.insert("answrs", ["msg", "answ"], [newMsg, newAnsw])
        answ = "Я добавить новый запрос '{0}', давай рискнем попробовать".format(newMsg)
    if answ == "":
        for i in database.get("answrs"):
            if msg == i["msg"]:
                answ = i["answ"]
                break
            else:
                answ = "Я не знаю такой команды. Можешь научить меня используя команду /teach (команда) ? (ответ)"
    elif msg == "/relax":
        answ = "Yeah! Бот уходить спатьки для вас, разбудите его командой /wake up"
        param = 1
    elif (msg == "/wake up") and (param == 1):
        answ = "Всем привет я только что проснулся, из-за вас"
        param = 0
    elif (msg == "/wake up") and (param == 0):
        answ = "Я не сплю, шо надо?"
    return HttpResponse("ok")
def sendAnswer(userID, answ = "", attach = "", keyboard = ""):
	vkAPI.messages.send(user_id = userID, message = answ, attachment=attach, keyboard=keyboard, random_id = random.randint(1, 99999999999999999), v=5.103)
def keyboardstart(request, userID):
	answ = "Привет! Выбери свою группу пользователя! Команды - /help"
	keyboard = json.dumps({
		"one_time": True,

		"buttons":[[
			{
				"action": {
					"type":"text",
					"label":"Админы",
					"payload": """{"command":"admins"}"""
				},
				"color":"positive"
			},
            {
				"action": {
					"type":"text",
					"label":"Модеры",
					"payload": """{"command":"moders"}"""
				},
				"color":"primary"
			},
            {
				"action": {
					"type":"text",
					"label":"Холопы",
					"payload": """{"command":"nothings"}"""
				},
				"color":"negative"
			}
		]]
	})
	


	sendAnswer(userID, answ, keyboard = keyboard)

lg = {
    "success":False,
    "groups":database.get('groups', ["groupName"])
}

def login(request):
    global lg

    if "admin" == request.GET.get("login") and "0000" == request.GET.get("password"):
        lg["success"]=True
    return render(request, "login.html", lg)