__author__ = 'Ugo'
# TODO. Al acceder al servidor que devuelva algún mensaje, como las parámetros que acepta
# La propiedad isAttached hay que calcularla correctamente
# Después de cada print debemos dejar un \n para que los mensajes de la consola no salgan superpuestos
# Implementar un servicio para reiniciar la conexion Serial para cuando desconectas y conectas el Arduino
# Implementar StopHAND
# Ver porque el Bicep cuando se attacha se sube completamente. Parece que en el MRLComm tiene un valor por defecto
# Implementar una propiedad de los servos para que cuando se llegue a la posición determinada hagan un detach y así no chirrien
# Los servos deben empezar por defecto con minima velocidad para que al conectar el robot no pegue tirones
# PArece que cuando hace el attach asigna como posicion la MIDDLE. Probamos-> velocidad a 0, attach, moveTo REST y velocidad a normal
# LA PRIMERA VEZ QUE HACES ATTACH CREA EL SERVO. LO QUE SE HAGA ANTES NO VALE PARA NADA
# PODEMOS CREAR UN ATACH Y DETACH RAPIDO PARA CREAR SERVO Y DESPUES ESTABLECEMOS PROPIEDADES
# Con la boca abierta roza la mandibula al girar el cuello
# En las funciones rest verificar antes si hay pin asignado, sino, no descansamos
# Ver lo que devuelven las funciones (muchas veces True o False) porque no esta claro
# isAttached habria que cambiarlo por una funcion que fuera isAllAttached or isAnyAttached excepto en los servos que puede ser una variable solo
# Cuando se setea la velocidad al hacer REST pasa por posicion 0

import arduinocontroller
import inmoovhand
import inmoovarm
import inmoovhead
import re
import googletts
import pyglet
import os
import chatruntime
import time
import random
import threading
import urllib
import json
import datetime

class InMoov():
    def __init__(self):
        self.context=""
        self.chatRuntime=chatruntime.ChatRuntime()
        self.autoDetachTimer=None
        self.runTimers=True
        self.soundCache={"soundIndex":1}
        time.sleep(1)
        self.loadSoundCache()

    def init(self, serialPort, baudRate):
        self.arduinoController=arduinocontroller.ArduinoController(serialPort, baudRate)
        self.rightHand=inmoovhand.InMoovHand(self.arduinoController)
        self.leftHand=inmoovhand.InMoovHand(self.arduinoController)
        self.rightArm=inmoovarm.InMoovArm(self.arduinoController)
        self.leftArm=inmoovarm.InMoovArm(self.arduinoController)
        self.head=inmoovhead.InMoovHead(self.arduinoController)

        if not self.arduinoController.initSerial():
            return False

        self.autoDetachTimer=threading.Thread(target=self.autoDetachTimerFunction)
        self.autoDetachTimer.start()
        return True

    def rest(self):
        print ("REST all servos")
        self.rightHand.rest()
        self.leftHand.rest()
        self.rightArm.rest()
        self.leftArm.rest()
        self.head.rest()

    def detach(self):
        self.rightHand.detach()
        self.leftHand.detach()
        self.rightArm.detach()
        self.leftArm.detach()
        self.head.detach()

    def autoDetachTimerFunction(self):
        while self.runTimers==True:
            # Cabeza
            if self.head.neck.isAttached and self.head.neck.autoDetachTime!=0 and self.head.neck.lastMoveTime+self.head.neck.autoDetachTime<time.time():
                self.head.neck.detach()
            if self.head.rotate.isAttached and self.head.rotate.autoDetachTime!=0 and self.head.rotate.lastMoveTime+self.head.rotate.autoDetachTime<time.time():
                self.head.rotate.detach()
            if self.head.jaw.isAttached and self.head.jaw.autoDetachTime!=0 and self.head.jaw.lastMoveTime+self.head.jaw.autoDetachTime<time.time():
                self.head.jaw.detach()
            if self.head.eyeX.isAttached and self.head.eyeX.autoDetachTime!=0 and self.head.eyeX.lastMoveTime+self.head.eyeX.autoDetachTime<time.time():
                self.head.eyeX.detach()
            if self.head.eyeY.isAttached and self.head.eyeY.autoDetachTime!=0 and self.head.eyeY.lastMoveTime+self.head.eyeY.autoDetachTime<time.time():
                self.head.eyeY.detach()
            # Brzo derecho
            if self.rightArm.bicep.isAttached and self.rightArm.bicep.autoDetachTime!=0 and self.rightArm.bicep.lastMoveTime+self.rightArm.bicep.autoDetachTime<time.time():
                self.rightArm.bicep.detach()
            if self.rightArm.rotate.isAttached and self.rightArm.rotate.autoDetachTime!=0 and self.rightArm.rotate.lastMoveTime+self.rightArm.rotate.autoDetachTime<time.time():
                self.rightArm.rotate.detach()
            if self.rightArm.shoulder.isAttached and self.rightArm.shoulder.autoDetachTime!=0 and self.rightArm.shoulder.lastMoveTime+self.rightArm.shoulder.autoDetachTime<time.time():
                self.rightArm.shoulder.detach()
            if self.rightArm.omoplate.isAttached and self.rightArm.omoplate.autoDetachTime!=0 and self.rightArm.omoplate.lastMoveTime+self.rightArm.omoplate.autoDetachTime<time.time():
                self.rightArm.omoplate.detach()
            # Mano derecha
            if self.rightHand.thumb.isAttached and self.rightHand.thumb.autoDetachTime!=0 and self.rightHand.thumb.lastMoveTime+self.rightHand.thumb.autoDetachTime<time.time():
                self.rightHand.thumb.detach()
            if self.rightHand.index.isAttached and self.rightHand.index.autoDetachTime!=0 and self.rightHand.index.lastMoveTime+self.rightHand.index.autoDetachTime<time.time():
                self.rightHand.index.detach()
            if self.rightHand.majeure.isAttached and self.rightHand.majeure.autoDetachTime!=0 and self.rightHand.majeure.lastMoveTime+self.rightHand.majeure.autoDetachTime<time.time():
                self.rightHand.majeure.detach()
            if self.rightHand.ringfinger.isAttached and self.rightHand.ringfinger.autoDetachTime!=0 and self.rightHand.ringfinger.lastMoveTime+self.rightHand.ringfinger.autoDetachTime<time.time():
                self.rightHand.ringfinger.detach()
            if self.rightHand.pinky.isAttached and self.rightHand.pinky.autoDetachTime!=0 and self.rightHand.pinky.lastMoveTime+self.rightHand.pinky.autoDetachTime<time.time():
                self.rightHand.pinky.detach()
            if self.rightHand.wrist.isAttached and self.rightHand.wrist.autoDetachTime!=0 and self.rightHand.wrist.lastMoveTime+self.rightHand.wrist.autoDetachTime<time.time():
                self.rightHand.wrist.detach()

            time.sleep(1)

    def saveSoundCache(self):
        json.dump(self.soundCache, open(os.path.dirname(os.path.abspath(__file__))+"/speechcache/index.json",'w'))

    def loadSoundCache(self):
        if not os.path.isfile(os.path.dirname(os.path.abspath(__file__))+"/speechcache/index.json"):
            return
        self.soundCache = json.load(open(os.path.dirname(os.path.abspath(__file__))+"/speechcache/index.json",'r'))

    def say (self, what):
        sentences=what.split(".")

        for sentence in sentences:
            sentence=sentence.strip()
            if sentence=="":
                continue

            print ("SAYING: ", sentence)
            path=os.path.dirname(os.path.abspath(__file__))+"/speechcache/"
            filename=sentence.lower().replace(" ", "")+".mp3"

            if not filename in self.soundCache:
                tts=googletts.googleTTS(text=''+sentence,lang='es', debug=False)
                tts.save(path+str(self.soundCache["soundIndex"])+".mp3")
                self.soundCache[filename]=str(self.soundCache["soundIndex"])+".mp3"
                self.soundCache["soundIndex"]=self.soundCache["soundIndex"]+1

            song = pyglet.media.load(path+self.soundCache[filename])
            song.play()
            time_speaking=song.duration-0.5
            start_time=time.time()

            while time.time()-start_time<time_speaking:
                pos=random.randrange(10,20)
                self.head.jaw.moveTo(pos)
                time.sleep(0.2)
                pos=random.randrange(30,50)
                self.head.jaw.moveTo(pos)
                time.sleep(0.2)
            self.head.jaw.moveTo(10)
            time.sleep(0.5)

    #######################################################################################
    # VOICE COMMAND FUNCTIONS
    #######################################################################################
    def wikipedia (self, moreInfo=False):
        if moreInfo==False:
            to_search=self.chatRuntime.rightWildcard
            self.lastWikipediaSearch=to_search
            self.lastWikipediaSentence=0
        else:
            to_search=self.lastWikipediaSearch
            self.lastWikipediaSentence=self.lastWikipediaSentence+1

        url="https://es.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="+to_search
        response = urllib.request.urlopen(url, timeout = 5)
        content = response.read()
        json_result=json.loads(str(content,"utf-8"))
        self.head.rotate.moveTo(90)
        self.head.neck.moveTo(90)
        try:
            plain_extract=json_result["query"]["pages"][list((json_result["query"]["pages"]).keys())[0]]["extract"]
            sentences=plain_extract.split(".")
            self.say(sentences[self.lastWikipediaSentence])
        except:
            if moreInfo==False:
                self.say("No encuentro información para el término "+to_search)
            else:
                self.say("No encuentro información adicional acerca de eso.")

    def time (self):
        now=datetime.datetime.now()
        hora=now.hour
        if hora>12:
            hora=hora-12

        time_text="Son las "
        time_text=time_text+str(hora)
        time_text=time_text+" y "
        time_text=time_text+str(now.minute)
        if now.hour>20:
            time_text=time_text+" de la noche"
        elif now.hour>12:
            time_text=time_text+" de la tarde"
        else:
            time_text=time_text+" de la mañana"
        self.head.rotate.moveTo(90)
        self.head.neck.moveTo(90)
        self.say(time_text)

    def date (self):
        now=datetime.datetime.now()

        date_text="Hoy es "
        date_text=date_text+self.chatRuntime.weekday[now.weekday()]+" "
        date_text=date_text+str(now.day)+" de "
        date_text=date_text+self.chatRuntime.month[now.month-1]+" de "
        date_text=date_text+str(now.year)
        self.head.rotate.moveTo(90)
        self.head.neck.moveTo(90)
        self.say(date_text)

    def age(self):
        now=datetime.datetime.now()
        dateofbirth=datetime.datetime(year=2015, month=8, day=15)
        date_text="Me creaste el "
        date_text=date_text+self.chatRuntime.weekday[dateofbirth.weekday()]+" "
        date_text=date_text+str(dateofbirth.day)+" de "
        date_text=date_text+self.chatRuntime.month[dateofbirth.month-1]+" de "
        date_text=date_text+str(dateofbirth.year)

        delta=now-dateofbirth
        date_text=date_text+", luego tengo "
        date_text=date_text+str(delta.days)
        date_text=date_text+" días de existencia"
        self.head.rotate.moveTo(90)
        self.head.neck.moveTo(90)
        self.say(date_text)

    def weather(self):
        url="http://api.openweathermap.org/data/2.5/weather?zip=41960,es"
        response = urllib.request.urlopen(url, timeout = 5)
        content = response.read()
        json_result=json.loads(str(content,"utf-8"))
        self.head.rotate.moveTo(90)
        self.head.neck.moveTo(90)
        try:
            current_temp=int(json_result["main"]["temp"]-272.15)
            max_temp=int(json_result["main"]["temp_max"]-272.15)
            min_temp=int(json_result["main"]["temp_min"]-272.15)
            weather_text="Actualmente hace "
            weather_text=weather_text+str(current_temp)+" grados. "
            weather_text=weather_text+"La máxima hoy será de "+str(max_temp)
            weather_text=weather_text+" y la mínima de "+str(min_temp)
            self.say(weather_text)
        except:
            self.say("¡Cortocircuitos! He tenido algún problema intentando contactar con el servicio de meteorología")

    def calculator (self):
        exp=self.chatRuntime.lastInput
        exp=exp.replace('más', '+')
        exp=exp.replace('menos', '-')
        res=eval(exp)
        self.say(str(res))

    def bye(self):
        self.say("Hasta otra Ugo. Espero verte pronto")
        self.head.rest()

    def voiceCommand(self, input):
        input=input.replace("uno", "1")
        input=input.replace("dos", "2")
        input=input.replace("tres", "3")
        input=input.replace("cuatro", "4")
        input=input.replace("cinco", "5")
        input=input.replace("seis", "6")
        input=input.replace("siete", "7")
        input=input.replace("ocho", "8")
        input=input.replace("nueve", "9")
        input=input.replace("diez", "10")

        result=self.chatRuntime.respond(input)
        if result==None:
            print ("No te entiendo, inténtalo de otra manera")
            self.say("No te entiendo, inténtalo de otra manera")
            return

        if result[0:5]=="PYCMD":
            exec (result[6:])
        else:
            print (result)
            self.say(result)

    def lookAndHello(self):
        self.head.neck.moveTo(95)
        self.head.rotate.moveTo(80)
        time.sleep(0.5)
        self.say("Hola Ugo. ¿Cómo va todo?")

    def cmdOpenHand(self, which):
        if which=="right" or which=="both":
            self.rightHand.setSpeed(100,100,100,100,100,100)
            self.rightHand.setAutoDetachTime(2)
            self.rightHand.open()
        if which=="left" or which=="both":
            self.leftHand.setSpeed(100,100,100,100,100,100)
            self.leftHand.setAutoDetachTime(2)
            self.leftHand.open()

    def cmdCloseHand(self, which, speed=""):
        if which=="right" or which=="both":
            if speed=='slowly':
                self.rightHand.setSpeed(80,82,86,80,80,80)
                self.rightHand.setAutoDetachTime(12)
            else:
                self.rightHand.setSpeed(100,100,100,100,100,100)
                self.rightHand.setAutoDetachTime(2)

            self.rightHand.close()
        if which=="left" or which=="both":
            if speed=='slowly':
                self.leftHand.setSpeed(80,80,82,80,80,80)
                self.leftHand.setAutoDetachTime(25)
            else:
                self.leftHand.setSpeed(100,100,100,100,100,100)
                self.leftHand.setAutoDetachTime(2)

            self.leftHand.close()

    def cmdStopHand(self, which):
        if which=="right" or which=="both":
            self.rightHand.detach()
        if which=="left" or which=="both":
            self.leftHand.detach()

    def cmdHeadUp(self):
        self.say("Levanto la cabeza")

    def cmdHeadDown(self):
        self.say("Bajo la cabeza")

    def cmdHeadRest(self):
        self.say("Pongo la cabeza en posición de reposo")

    def cmdGreet(self):
        self.say("¡Hola! ¿Cómo estás?")

    def cmdTakeThis(self):
        self.head.rotate.moveTo(95)
        self.head.neck.moveTo(45)
        self.rightArm.omoplate.moveTo(20)
        self.rightArm.shoulder.moveTo(57)
        self.rightArm.rotate.moveTo(48)
        self.rightArm.bicep.moveTo(43)
        self.rightHand.wrist.moveTo(180)
        self.rightHand.open()

    def cmdArmForward(self, which):
        self.head.rotate.moveTo(90)
        self.head.neck.moveTo(80)
        if which=="right" or which=="both":
            self.rightArm.omoplate.moveTo(20)
            self.rightArm.shoulder.moveTo(96)
            self.rightArm.rotate.moveTo(0)
            self.rightArm.bicep.moveTo(0)
            self.rightHand.wrist.moveTo(180)
        if which=="left" or which=="both":
            self.leftArm.omoplate.moveTo(20)
            self.leftArm.shoulder.moveTo(96)
            self.leftArm.rotate.moveTo(0)
            self.leftArm.bicep.moveTo(0)
            self.leftHand.wrist.moveTo(180)

    def cmdCountTo(self, number=None):
        if number is None:
            if self.chatRuntime.rightWildcard not in ["1","2","3","4","5","6","7","8","9","10"]:
                self.head.rotate.moveTo(90)
                self.head.neck.moveTo(90)
                self.say("Sólo se contar hasta 10")
                return
            number=self.chatRuntime.rightWildcard
        number=int(number)
        self.head.rotate.moveTo(68)
        self.head.neck.moveTo(40)
        self.rightArm.omoplate.moveTo(20)
        self.rightArm.shoulder.moveTo(10)
        self.rightArm.rotate.moveTo(130)
        self.rightArm.bicep.moveTo(80)
        self.rightHand.wrist.moveTo(0)
        self.rightHand.open()
        time.sleep(1)
        self.rightHand.close()
        time.sleep(3)
        self.rightHand.index.moveTo(0)
        self.say("uno")
        if number>1:
            time.sleep(0.5)
            self.rightHand.majeure.moveTo(0)
            self.say("dos")
        if number>2:
            time.sleep(0.5)
            self.rightHand.ringfinger.moveTo(0)
            self.say("tres")
        if number>3:
            time.sleep(0.5)
            self.rightHand.pinky.moveTo(0)
            self.say("cuatro")
        if number>4:
            time.sleep(0.5)
            self.rightHand.thumb.moveTo(0)
            self.say("cinco")
        if number>5: # Solo tengo un brazo para contar!!!
            self.head.rotate.moveTo(119)
            time.sleep(1.5)
            self.head.rotate.moveTo(68)
            time.sleep(1.5)
            self.head.rotate.moveTo(119)
            time.sleep(1.5)
            self.head.rotate.moveTo(90)
            self.head.neck.moveTo(90)
            self.say("¡Chispas! Sólo tengo un brazo. No puedo contar más de 5")

        self.head.rotate.moveTo(90)
        self.head.neck.moveTo(90)
