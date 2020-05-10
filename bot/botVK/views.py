from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import json
import vk
import random
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
        msg = body['object']['message']["text"]
        answ = ""
        param = 0
        attach = ""
        #userinfo = vkAPI.users.get(user_ids = userID, v=5.103)[0]
        
        sendAnswer(userID, answ, attach)
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
    elif msg == "/list":
        conn  = sqlite3.connect('db.sqlite')
        cur = conn.cursor()
        query="""
        SELECT * FROM answer
        """
        cur.execute(query)
        answ = cur.fetchall()
        conn.close()
def sendAnswer(userID, answ = "", attach = ""):
	vkAPI.messages.send(user_id = userID, message = answ, attachment=attach, random_id = random.randint(1, 99999999999999999), v=5.103)