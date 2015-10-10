__author__ = 'Ugo'
import re

commandsDatabase = [
#   ["key", "pattern", "context", "response"]
#   key = identificador de este registro para usarlo como context condicional en context
#   pattern = expresión regular que debe cumplir la frase de entrada
#   context = si no está vacío este registro aplicará sólo cuando el contexto (key de la frase anterior) sea el indicado
#   response = respuesta del robot
    # Saludo
    ["howareyou", "(.*)(hola|que pasa|cómo va)(.*)","","PYCMD self.lookAndHello()"],
    ["", "(.*)(bien|maravilla|perfecto|guay)(.*)","howareyou","Me alegro"],
    ["", "(.*)(mal|regular|triste)(.*)","howareyou","Vaya. Espero que todo se arregle"],
    ["", "(.*)(sueño)(.*)","howareyou","Necesitas dormir más"],
    ["", "(.*)(aburrido)(.*)","howareyou","Te podría contar un chiste. Pero no me has programado para ello"],

    # Despedida
    ["", "(.*)(adios|hasta luego|hasta otra|nos vemos)(.*)","","PYCMD self.bye()"],

    # ¿Cuál es tu nombre?
    ["", "(.*)(cómo)(.*)(llamas)(.*)","","Me llamo Supercool. Tu me pusiste ese nombre"],
    ["", "(.*)(cuál)(.*)(nombre)(.*)","","Me llamo Supercool. Tu me pusiste ese nombre"],

    # Edad
    ["whenyoucreatedme", "(.*)(cuál|qué|que)(.*)(edad)(.*)","","PYCMD self.age()"],
    ["whenyoucreatedme", "(.*)(años)(.*)(tienes)(.*)","","PYCMD self.age()"],

    # ¿Qué sabes hacer?
    ["", "(.*)(sabes)(.*)(hacer)(.*)","","Por ahora no se hacer mucho. Sólo intentar responderte a tus preguntas"],

    # Wikipedia
    ["wikipedia", "(.*)(significado de)(.*)(palabra)(.*)","","PYCMD self.wikipedia()"],
    ["wikipedia", "(.*)(significado de)(.*)","","PYCMD self.wikipedia()"],
    ["wikipedia", "(.*)(significa)(.*)","","PYCMD self.wikipedia()"],
    ["wikipedia", "(.*)(wikipedia|internet)(.*)(palabra)(.*)","","PYCMD self.wikipedia()"],
    ["wikipedia", "(.*)(wikipedia|internet)(.*)","","PYCMD self.wikipedia()"],
    ["wikipedia", "(.*)(qué|que)(.*)(sabes|decirme)(.*)(de)(.*)","","PYCMD self.wikipedia()"],
    ["wikipedia", "(.*)(más|mas)(.*)(detalle|info|información|datos)(.*)","wikipedia","PYCMD self.wikipedia(True)"],

    # Hora
    ["", "(.*)(tienes|tiene)(.*)(hora)(.*)","","PYCMD self.time()"],
    ["", "(.*)(hora)(.*)(es)(.*)","","PYCMD self.time()"],
    ["", "(.*)(dime|dices)(.*)(hora)(.*)","","PYCMD self.time()"],

    # Día
    ["", "(.*)(fecha|dia|día)(.*)(hoy|actual|estamos)(.*)","","PYCMD self.date()"],

    # Tiempo
    ["", "(.*)(qué|que)(.*)(tiempo)(.*)(hoy)(.*)","","PYCMD self.weather()"],

    # Abrir mano
    ["", "(.*)(abrir|abre|abres)(.*)(dos|ambas|todas)(.*)(mano|manita)(.*)", "", "PYCMD self.cmdOpenHand ('both')"],
    ["", "(.*)(abrir|abre|abres)(.*)(mano|manita)(.*)(derecha)(.*)", "", "PYCMD self.cmdOpenHand ('right')"],
    ["", "(.*)(abrir|abre|abres)(.*)(mano|manita)(.*)(izquierda)(.*)", "", "PYCMD self.cmdOpenHand ('left')"],
    ["openhand", "(.*)(abrir|abre|abres)(.*)(mano|manita)(.*)", "", "¿Qué mano quieres que abra?"],
    ["", "(.*)(dos|ambas|todas)(.*)", "openhand", "PYCMD self.cmdOpenHand ('both')"],
    ["", "(.*)(derecha)(.*)", "openhand", "PYCMD self.cmdOpenHand ('right')"],
    ["", "(.*)(izquierda)(.*)", "openhand", "PYCMD self.cmdOpenHand ('left')"],
    ["", "(.*)", "openhand", "No entiendo que mano quieres que abra"],

    # Cerrar mano despacio
    ["closebothhandslowly", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(despacio|despacito|poco a poco)(.*)(dos|ambas|todas)(.*)(mano|manita)(.*)", "", "PYCMD self.cmdCloseHand ('right', 'slowly')"],
    ["closerighthandslowly", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(mano|manita)(.*)(derecha)(.*)(despacio|despacito|poco a poco)(.*)", "", "PYCMD self.cmdCloseHand ('right', 'slowly')"],
    ["closerighthandslowly", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(despacio|despacito|poco a poco)(.*)(mano|manita)(.*)(derecha)(.*)", "", "PYCMD self.cmdCloseHand ('right', 'slowly')"],
    ["closelefthandslowly", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(mano|manita)(.*)(izquierda)(.*)(despacio|despacito|poco a poco)(.*)", "", "PYCMD self.cmdCloseHand ('left', 'slowly')"],
    ["closelefthandslowly", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(despacio|despacito|poco a poco)(.*)(mano|manita)(.*)(izquierda)(.*)", "", "PYCMD self.cmdCloseHand ('left', 'slowly')"],
    ["closehandslowly", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(mano|manita)(.*)(despacio|despacito|poco a poco)(.*)", "", "¿Qué mano quieres que cierre poco a poco?"],
    ["closebothhandslowly", "(.*)(dos|ambas|todas)(.*)", "closehandslowly", "PYCMD self.cmdCloseHand ('both', 'slowly')"],
    ["closerighthandslowly", "(.*)(derecha)(.*)", "closehandslowly", "PYCMD self.cmdCloseHand ('right', 'slowly')"],
    ["closelefthandslowly", "(.*)(izquierda)(.*)", "closehandslowly", "PYCMD self.cmdCloseHand ('left', 'slowly')"],
    ["", "(.*)", "closehandslowly", "No entiendo que mano quieres que cierre"],
    ["", "(.*)(ya|para|basta|stop|listo)(.*)", "closebothhandslowly", "PYCMD self.cmdStopHand ('both')"],
    ["", "(.*)(ya|para|basta|stop|listo)(.*)", "closerighthandslowly", "PYCMD self.cmdStopHand ('right')"],
    ["", "(.*)(ya|para|basta|stop|listo)(.*)", "closelefthandslowly", "PYCMD self.cmdStopHand ('left')"],

    # Cerrar mano
    ["", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(dos|ambas|todas)(.*)(mano|manita)(.*)", "", "PYCMD self.cmdCloseHand ('both')"],
    ["", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(mano|manita)(.*)(derecha)(.*)", "", "PYCMD self.cmdCloseHand ('right')"],
    ["", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(mano|manita)(.*)(izquierda)(.*)", "", "PYCMD self.cmdCloseHand ('left')"],
    ["closehand", "(.*)(cerrar|cierra|cierras|serrar|sierra|sierras)(.*)(mano|manita)(.*)", "", "¿Qué mano quieres que cierre?"],
    ["", "(.*)(dos|ambas|todas)(.*)", "openhand", "PYCMD self.cmdCloseHand ('both')"],
    ["", "(.*)(derecha)(.*)", "closehand", "PYCMD self.cmdCloseHand ('right')"],
    ["", "(.*)(izquierda)(.*)", "closehand", "PYCMD self.cmdCloseHand ('left')"],
    ["", "(.*)", "closehand", "No entiendo que mano quieres que cierre"],

    # Coge esto
    ["", "(.*)(toma|coge)(.*)(esto|esta)(.*)", "", "PYCMD self.cmdTakeThis ()"],

    # Extender el brazo adelante
    ["", "(.*)(pon|extiende|mueve)(.*)(brazo)(.*)(izquierdo)(.*)(adelante|delante)(.*)", "", "PYCMD self.cmdArmForward ('left')"],
    ["", "(.*)(pon|extiende|mueve)(.*)(brazo)(.*)(derecho)(.*)(adelante|delante)(.*)", "", "PYCMD self.cmdArmForward ('right')"],
    ["", "(.*)(pon|extiende|mueve)(.*)(adelante|delante)(.*)(brazo)(.*)(izquierdo)(.*)", "", "PYCMD self.cmdArmForward ('left')"],
    ["", "(.*)(pon|extiende|mueve)(.*)(adelante|delante)(.*)(brazo)(.*)(derecho)(.*)", "", "PYCMD self.cmdArmForward ('right')"],
    ["", "(.*)(pon|extiende|mueve)(.*)(brazo)(.*)(dos|ambos|todos)(.*)(adelante|delante)(.*)", "", "PYCMD self.cmdArmForward ('both')"],
    ["armforward", "(.*)(pon|extiende|mueve)(.*)(brazo)(.*)(adelante|delante)", "", "¿Qué brazo quieres que mueva?"],
    ["", "(.*)(dos|ambas|todas)(.*)", "openhand", "PYCMD self.cmdArmfForward ('both')"],
    ["", "(.*)(derecha)(.*)", "armforward", "PYCMD self.cmdArmForward ('right')"],
    ["", "(.*)(izquierda)(.*)", "armforward", "PYCMD self.cmdArmForward ('left')"],
    ["", "(.*)", "armforward", "No entiendo que brazo quieres que mueva"],

    # Bajar el brazo
    ["", "(.*)(baja)(.*)(brazo)(.*)(izquierdo)(.*)", "", "PYCMD self.leftArm.rest()"],
    ["", "(.*)(baja)(.*)(brazo)(.*)(derecho)(.*)", "", "PYCMD self.rightArm.rest()"],
    ["restarm", "(.*)(baja)(.*)(brazo)(.*)", "", "¿Qué brazo quieres que baje?"],
    #["", "(.*)(dos|ambas|todas)(.*)", "openhand", "PYCMD self.cmdArmfForward ('both')"],
    ["", "(.*)(derecho)(.*)", "restarm", "PYCMD self.rightArm.rest()"],
    ["", "(.*)(izquierdo)(.*)", "restarm", "PYCMD self.leftArms.rest()"],
    ["", "(.*)", "restarm", "No entiendo que brazo quieres que baje"],






    # Levantar cabeza
    ["", "(.*)(levantar|levanta|levantas|subir|sube|subes)(.*)(cabeza|cabecita)(.*)", "", "PYCMD self.cmdHeadUp ()"],
    # Agachar cabeza
    ["", "(.*)(bajar|baja|bajas|agachar|agacha|agachas)(.*)(cabeza|cabecita)(.*)", "", "PYCMD self.cmdHeadDown ()"],
    # Reposar cabeza
    ["", "(.*)(cabeza|cabecita)(.*)(posición)(.*)(descanso|descansar|normal|reposo)", "", "PYCMD self.cmdHeadRest ()"],
    ["", "(.*)(descansar|descansa|descansas)(.*)(cabeza|cabecita)(.*)", "", "PYCMD self.cmdHeadRest ()"],
    ["", "(.*)(pon|pones|deja)(.*)(normal|resposo)(.*)(cabeza|cabecita)(.*)", "", "PYCMD self.cmdHeadRest ()"],
    ["", "(.*)(pon|pones|deja)(.*)(cabeza|cabecita)(.*)(normal|resposo)(.*)", "", "PYCMD self.cmdHeadRest ()"],
    # Saludar
    ["", "(.*)(saludar|saluda|saludas)(.*)", "", "PYCMD self.cmdGreet()"],
    ["", "(.*)(hola|que pasa|que te cuentas)(.*)", "", "PYCMD self.cmdGreet()"],
    # Contar
    ["", "(.*)(contar|cuenta|cuentas)(.*)(hasta)(.*)", "", "PYCMD self.cmdCountTo()"],
    ["countto", "(.*)(contar|cuenta|cuentas)(.*)", "", "¿Hasta cuánto quieres que cuente?"],
    ["", "(.*)(uno)(.*)", "countto", "PYCMD self.cmdCountTo('one')"],
    ["", "(.*)(dos)(.*)", "countto", "PYCMD self.cmdCountTo('two')"],
    ["", "(.*)(tres)(.*)", "countto", "PYCMD self.cmdCountTo('three')"],
    ["", "(.*)(cuatro)(.*)", "countto", "PYCMD self.cmdCountTo('four')"],
    ["", "(.*)(cinco)(.*)", "countto", "PYCMD self.cmdCountTo('five')"],
    ["", "(.*)(seis)(.*)", "countto", "PYCMD self.cmdCountTo('six')"],
    ["", "(.*)(siete)(.*)", "countto", "PYCMD self.cmdCountTo('seven')"],
    ["", "(.*)(ocho)(.*)", "countto", "PYCMD self.cmdCountTo('eight')"],
    ["", "(.*)(nueve)(.*)", "countto", "PYCMD self.cmdCountTo('nine')"],
    ["", "(.*)(diez)(.*)", "countto", "PYCMD self.cmdCountTo('ten')"],
    ["", "(.*)", "countto", "Sólo se contar hasta diez"],


    # Descansa
    ["", "(.*)(descansa|reposo)(.*)", "", "PYCMD self.rest()"],
    # CALCULADORA. TODO!!!!
    ["","(.*)[0-9][ ](más|menos)[ ][0-9](.*)","","PYCMD self.calculator()"]
]

class ChatRuntime:
    def __init__(self):
        self.commandsDatabase=commandsDatabase
        self.context=""
        self.lastInput=""
        self.lastRegExp=""
        self.rightWildcard=""
        self.month=["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
        self.weekday=["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]


    def respond (self, input):
        index=0
        input=input.lower()
        self.lastInput=input

        for command in self.commandsDatabase:
            if command[2]==self.context or command[2]=="":
                #print ("CHECK RE: ", command[1], "\n")

                p = re.compile(command[1], re.IGNORECASE)
                if p.match(input)!=None:
                    self.context=command[0]
                    self.lastRegExp=command[1]
                    #print ("CHECK RE: ", command[1], "\n")
                    #print ("CURRENT CONTEXT: ", self.context, "\n")
                    #print ("CMD: ", command[3], "\n")
                    self.fillCommandAtributes()
                    return command[3]
        self.context=""
        self.lastRegExp=""
        return (None)

    def fillCommandAtributes(self):
        # (.*) derecha
        if self.lastRegExp[-4:]=="(.*)":
            right_text=re.sub(self.lastRegExp[0:-4],"", self.lastInput)
            self.rightWildcard=right_text.strip()
        else:
            self.rightWildcard=""
        return