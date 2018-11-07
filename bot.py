from fbchat import Client
from fbchat.models import *
from bs4 import BeautifulSoup
from requests import get
import random, time, datetime, json, requests, os, sys
import numpy as np


email = ""
password = ""

ryz = "2304717856220410"
meine = "1536442066412320"
swider = "100002268938732"
korsan = "100024773796503"
mojeid = "100007813848151"

headers = {
    'Content-Type': "application/json",
    'x-api-key': "bffd8b8b-cfa0-4d1a-8f6b-ba9207dc6c79"
}


class WiertarBot(Client):
    banned = np.load("banned.npy").tolist()
    gamelist = np.load("games.npy").tolist()
    ryz_commands = False
    weather_key = ""

    def mentions(self, thread_id):
        thread = list(self.fetchThreadInfo(thread_id)[thread_id].participants)
        mention = []
        for i in range(len(thread)):
            mention.append(Mention(thread[i], 0, 9))
        return mention

    def onNicknameChange(self, mid=None, author_id=None, changed_for=None, new_nickname=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        if author_id != self.uid:
            if changed_for == self.uid:
                if new_nickname != np.load("nazwa.npy"):
                    abcdef = np.load("nazwa.npy")
                    self.changeNickname(str(abcdef), str(self.uid), str(thread_id), thread_type)

    def onListenError(self, exception=None):
        print(exception)
        if self.isLoggedIn():
            pass
        else:
            self.login(email, password)

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None,
                  thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        # self.markAsDelivered(thread_id, message_object.uid)
        # self.markAsRead(thread_id)
        print(message_object)
        print(message_object.text)
        if author_id in self.banned and author_id != mojeid:
            pass
                if message_object.text[0:6].lower() == "!bomb ":
                    a = message_object.text.split(" ")
                    parameters = {"inputUserMobile": a[1]}
                    self.send(Message("Zaczynam wysyłać"), thread_id, thread_type)
                    for i in range(int(a[2])):
                        adres = "http://gry.wapster.pl/ma/send.aspx?src=wap2&fid="+str(random.choice(self.gamelist))+"&r=LPH"
                        r = requests.post(adres, data=parameters)
                    self.send(Message("Wysłano "+a[2]+" wiadomosci na numer "+a[1]), thread_id, thread_type)
                
                pass

    
            if message_object.text[0:15].lower() == "poprosze tencze":
                if author_id == mojeid:
                    for i in range(10):
                        self.changeThreadColor(random.choice(kolorki), thread_id)
                    self.changeThreadColor(ThreadColor.BRILLIANT_ROSE, thread_id)
                    self.changeThreadColor(ThreadColor.BRILLIANT_ROSE, thread_id)
                else:
                    self.send(Message("Sam sobie zrób tęczę."), thread_id, thread_type)
                    
            elif message_object.text.lower() == "czas":
                now = datetime.datetime.now()
                tera = now.strftime("%A %d %B %H:%M")
                tera = tera.replace("September", "Września")
                tera = tera.replace("August", "Sierpnia")
                tera = tera.replace("October", "Października")
                tera = tera.replace("November", "Listopada")
                tera = tera.replace("Saturday", "Sobota")
                tera = tera.replace("Sunday", "Niedziela")
                tera = tera.replace("Monday", "Poniedziałek")
                tera = tera.replace("Tuesday", "Wtorek")
                tera = tera.replace("Wednesday", "Środa")
                tera = tera.replace("Thursday", "Czwartek")
                tera = tera.replace("Friday", "Piątek")
                czas = round(time.time())-3600
                czasdoswiat = 1545429600 - czas
                czasdowakacji = 1561068000 - czas
                wiadomosc = "Jest: " + tera + "\nPoczątek przerwy świątecznej (22 grudnia) za: " + str(int((czasdoswiat - czasdoswiat % 86400) / 86400)) + "dni " + time.strftime("%Hh %Mmin %Ssek", time.gmtime(int(round(czasdoswiat))))\
                            + "\nKoniec roku szkolnego za: " + str(int((czasdowakacji - czasdowakacji % 86400) / 86400)) + "dni " + time.strftime("%Hh %Mmin %Ssek", time.gmtime(int(round(czasdowakacji))))
                self.send(Message(wiadomosc), thread_id, thread_type)
            
            if author_id == mojeid or author_id == korsan or author_id == swider:
                if "@everyone" in message_object.text.lower():
                    self.send(Message("@everyone", self.mentions(thread_id)), thread_id, thread_type)

   
                
            if "spierdalaj" == message_object.text.lower():
                self.send(Message("sam spierdalaj"), thread_id, thread_type)
                self.reactToMessage(mid, MessageReaction.ANGRY)
            elif message_object.text.lower()[0:3] == "sam" and message_object.text.lower().endswith("spierdalaj"):
                t = message_object.text.lower().replace("sam", "")
                t = t.replace(" ", "")
                t = t.replace("spierdalaj", "")
                if t == "" and message_object.text.lower().count("spierdalaj") == 1:
                    message = "sam "
                    for i in range(message_object.text.lower().count("sam")):
                        message += "sam "
                    message += "spierdalaj"
                    self.send(Message(message), thread_id, thread_type)
                    self.reactToMessage(mid, MessageReaction.ANGRY)

 
 

bot = WiertarBot(email, password)
bot.listen()
