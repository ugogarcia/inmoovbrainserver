import gtts
import pyglet
import urllib
import io
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import time
import main
import inmoov
import json
import os
import googletts
import ssl

hostName = "localhost"
hostPort = 8443
serverVersion="0.1"

def execute(code):
    import sys
    fake_stdout = io.StringIO()
    __stdout = sys.stdout
    sys.stdout = fake_stdout

    try:
        #try if this is expressions
        ret = eval(code) #, globals(), locals())
        result = fake_stdout.getvalue()
        sys.stdout = __stdout
        if ret:
            result += str(ret)
        return result
    except:
        try:
            exec(code) #, globals(), locals())
        except:
            sys.stdout = __stdout
            import traceback
            buf = io.StringIO()
            traceback.print_exc(file=buf)
            return "ERROR: "+buf.getvalue()
        else:
            sys.stdout = __stdout
            return fake_stdout.getvalue()

def do_runpythoncmd (response, cmd):
    res=execute(cmd)
    response.wfile.write(bytes(res, "utf-8"))

def do_getservopositions (response):
    positions={}
    positions["leftarm_omoplate"]=myInMoov.leftArm.omoplate.currentPos
    positions["leftarm_shoulder"]=myInMoov.leftArm.shoulder.currentPos
    positions["leftarm_rotate"]=myInMoov.leftArm.rotate.currentPos
    positions["leftarm_bicep"]=myInMoov.leftArm.bicep.currentPos
    positions["lefthand_wrist"]=myInMoov.leftHand.wrist.currentPos
    positions["lefthand_thumb"]=myInMoov.leftHand.thumb.currentPos
    positions["lefthand_index"]=myInMoov.leftHand.index.currentPos
    positions["lefthand_majeure"]=myInMoov.leftHand.majeure.currentPos
    positions["lefthand_ringfinger"]=myInMoov.leftHand.ringfinger.currentPos
    positions["lefthand_pinky"]=myInMoov.leftHand.pinky.currentPos
    positions["rightarm_omoplate"]=myInMoov.rightArm.omoplate.currentPos
    positions["rightarm_shoulder"]=myInMoov.rightArm.shoulder.currentPos
    positions["rightarm_rotate"]=myInMoov.rightArm.rotate.currentPos
    positions["rightarm_bicep"]=myInMoov.rightArm.bicep.currentPos
    positions["righthand_wrist"]=myInMoov.rightHand.wrist.currentPos
    positions["righthand_thumb"]=myInMoov.rightHand.thumb.currentPos
    positions["righthand_index"]=myInMoov.rightHand.index.currentPos
    positions["righthand_majeure"]=myInMoov.rightHand.majeure.currentPos
    positions["righthand_ringfinger"]=myInMoov.rightHand.ringfinger.currentPos
    positions["righthand_pinky"]=myInMoov.rightHand.pinky.currentPos
    positions["head_neck"]=myInMoov.head.neck.currentPos
    positions["head_rotate"]=myInMoov.head.rotate.currentPos
    positions["head_jaw"]=myInMoov.head.jaw.currentPos
    positions["head_eyex"]=myInMoov.head.eyeX.currentPos
    positions["head_eyey"]=myInMoov.head.eyeY.currentPos
    response.wfile.write(bytes(json.dumps(positions), "utf-8"))

def do_getservostatus (response):
    status={}
    status["leftarm"]=myInMoov.leftArm.isAttached
    status["lefthand"]=myInMoov.leftHand.isAttached
    status["rightarm"]=myInMoov.rightArm.isAttached
    status["righthand"]=myInMoov.rightHand.isAttached
    status["head"]=myInMoov.head.isAttached
    response.wfile.write(bytes(json.dumps(status), "utf-8"))

def do_getserverstatus (response):
    status={}
    status["status"]="running"
    status["version"]=serverVersion
    response.wfile.write(bytes(json.dumps(status), "utf-8"))
    
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        # Obtenemos comando y parámetros
        pars=""
        pos=self.path.find("/",1)
        if pos==-1:
            cmd=self.path[1:].lower()
        else:
            cmd=self.path[1:pos].lower()
            pars=urllib.parse.unquote(self.path[pos+1:])

        #do_runvoicecmd(self,"hola esto es una prueba")

        # Procesamos comando y actuamos
        if cmd=="runpythoncmd":
            do_runpythoncmd(self, pars)
        elif cmd=="getservopositions":
            do_getservopositions(self)
        elif cmd=="getservostatus":
            do_getservostatus(self)
        elif cmd=="getserverstatus":
            do_getserverstatus(self)

print ("Running setup...")

#thing="Hola que tal"
#path=os.path.dirname(os.path.abspath(__file__))+"/speech/"
#tts=googletts.googleTTS(text=''+thing,lang='en', debug=True)
#tts.save(path+"speech.mp3")
#song = pyglet.media.load(path+"speech.mp3")
#song.play()
#quit()


myInMoov=inmoov.InMoov()
if not main.setup(myInMoov):
    print ("Error during setup. Exiting...")
    quit()
    # Ver los exiting codes of quit a ver que significan

print ("Starting server...")
myServer = HTTPServer((hostName, hostPort), MyServer)
myServer.socket = ssl.wrap_socket (myServer.socket, certfile='localhost.pem', server_side=True)
print("Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print("Server Stops - %s:%s" % (hostName, hostPort))





