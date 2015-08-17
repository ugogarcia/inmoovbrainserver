__author__ = 'Ugo'
# TODO. Al acceder al servidor que devuelva algún mensaje, como las parámetros que acepta
# La propiedad isAttached hay que calcularla correctamente
# Después de cada print debemos dejar un \n para que los mensajes de la consola no salgan superpuestos
import arduinocontroller
import inmoovhand
import inmoovarm
import inmoovhead
import re
import googletts
import pyglet
import os

voiceCommands = [
    ["main", "(.*)(abrir|abre|abres)(.*)(mano|manita)(.*)", "cmdOpenHand"],
    ["pars", "(.*)(abrir|abre|abres)(.*)(dos|ambas|todas)(.*)(mano|manita)(.*)", "both"],
    ["pars", "(.*)(abrir|abre|abres)(.*)(mano|manita)(.*)(derecha)(.*)", "righthand"],
    ["pars", "(.*)(abrir|abre|abres)(.*)(mano|manita)(.*)(izquierda)(.*)", "lefthand"],
    ["main", "(.*)(cerrar|cierra|cierras)(.*)(mano|manita)(.*)", "cmdCloseHand"],
    ["pars", "(.*)(cerrar|cierra|cierras)(.*)(dos|ambas|todas)(.*)(mano|manita)(.*)", "both"],
    ["pars", "(.*)(cerrar|cierra|cierras)(.*)(mano|manita)(.*)(derecha)(.*)", "righthand"],
    ["pars", "(.*)(cerrar|cierra|cierras)(.*)(mano|manita)(.*)(izquierda)(.*)", "lefthand"],
    ["main", "(.*)(levantar|levanta|levantas|subir|sube|subes)(.*)(cabeza|cabecita)(.*)", "cmdHeadUp"],
    ["main", "(.*)(bajar|baja|bajas|agachar|agacha|agachas)(.*)(cabeza|cabecita)(.*)", "cmdHeadDown"],
    ["main", "(.*)(cabeza|cabecita)(.*)(posición)(.*)(descanso|descansar|normal|reposo)", "cmdHeadRest"],
    ["main", "(.*)(descansar|descansa|descansas)(.*)(cabeza|cabecita)(.*)", "cmdHeadRest"],
    ["main", "(.*)(saludar|saluda|saludas)(.*)", "cmdGreet"],
    ["main", "(.*)(extender|extiende|extiendes)(.*)(mano|manita)(.*)", "cmdExtendHand"],
    ["pars", "(.*)(extender|extiende|extiendes)(.*)(dos|ambas|todas)(.*)(mano|manita)(.*)", "both"],
    ["pars", "(.*)(extender|extiende|extiendes)(.*)(mano|manita)(.*)(derecha)(.*)", "righthand"],
    ["pars", "(.*)(extender|extiende|extiendes)(.*)(mano|manita)(.*)(izquierda)(.*)", "lefthand"],
    ["main", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)", "cmdCountTo"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "one"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "two"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "three"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "four"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "five"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "six"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "seven"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "eight"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "nine"],
    ["pars", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)(uno)(.*)", "ten"]
]

class InMoov():
    def init(self, serialPort, baudRate):
        self.arduinoController=arduinocontroller.ArduinoController(serialPort, baudRate)
        self.rightHand=inmoovhand.InMoovHand(self.arduinoController)
        self.leftHand=inmoovhand.InMoovHand(self.arduinoController)
        self.rightArm=inmoovarm.InMoovArm(self.arduinoController)
        self.leftArm=inmoovarm.InMoovArm(self.arduinoController)
        self.head=inmoovhead.InMoovHead(self.arduinoController)

        if not self.arduinoController.initSerial():
            return False
        return True

    def rest(self):
        print ("REST all servos")
        self.rightHand.rest()
        self.leftHand.rest()
        self.rightArm.rest()
        self.leftArm.rest()
        self.head.rest()

    def say (self, thing):
        path=os.path.dirname(os.path.abspath(__file__))+"/speechcache/"
        filename=thing.lower().replace(" ", "")+".mp3"
        if not os.path.isfile(path+filename):
            tts=googletts.googleTTS(text=''+thing,lang='es', debug=False)
            tts.save(path+filename)
        song = pyglet.media.load(path+filename)
        song.play()

    def voiceCommand(self, cmd):
        index=0
        cmd=cmd.lower()
        match=False
        for command in voiceCommands:
            if command[0]=="main":
                p = re.compile(command[1], re.IGNORECASE)
                if p.match(cmd)!=None:
                    pars=[]
                    end=False
                    n=index+1
                    while not end:
                        if n>=len(voiceCommands) or voiceCommands[n][0]!="pars":
                            end=True
                        else:
                            p = re.compile(voiceCommands[n][1], re.IGNORECASE)
                            if p.match(cmd)!=None:
                                pars.append(voiceCommands[n][2])
                        n=n+1
                    #print ("VOICE COMMAND: ", command[2], ". PARS: ", pars)
                    exec ("self."+command[2]+"("+str(pars)+")")
                    match=True
            index=index+1
        if match==False:
            self.say("No te entiendo, inténtalo de otra manera")

    def cmdOpenHand(self, pars):
        print ("OPEN HAND: ", pars)
        if "righthand" in pars:
            self.say("Abro la mano derecha")
        elif "lefthand" in pars:
            self.say("Abro la mano izquierda")
        elif "both" in pars:
            self.say("Abro las dos manos")
        else:
            self.say("Tienes que decirme que mano abrir")

    def cmdCloseHand(self, pars):
        print ("CLOSE HAND: ", pars)
        if "righthand" in pars:
            self.say("Cierro la mano derecha")
        elif "lefthand" in pars:
            self.say("Cierro la mano izquierda")
        elif "both" in pars:
            self.say("Cierro las dos manos")
        else:
            self.say("Tienes que decirme que mano cerrar")

    def cmdHeadUp(self, pars):
        print ("HEAD UP: ", pars)
        self.say("Levanto la cabeza")

    def cmdHeadDown(self, pars):
        print ("HEAD DOWN: ", pars)
        self.say("Bajo la cabeza")

    def cmdHeadRest(self, pars):
        print ("HEAD REST: ", pars)
        self.say("Pongo la cabeza en posición de reposo")

    def cmdGreet(self, pars):
        print ("GREET: ", pars)
        self.say("¡Hola! ¿Cómo estás?")

    def cmdExtendHand(self, pars):
        print ("CLOSE HAND: ", pars)
        if "righthand" in pars:
            self.say("Extiendo la mano derecha")
        elif "lefthand" in pars:
            self.say("Extiendo la mano izquierda")
        elif "both" in pars:
            self.say("Extiendo las dos manos")
        else:
            self.say("Tienes que decirme que mano extender")

    def cmdCountTo(self, pars):
        print ("COUNT TO: ", pars)
        self.say("Contando")
