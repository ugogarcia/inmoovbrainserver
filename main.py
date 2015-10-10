__author__ = 'Ugo'
import arduinocontroller
import servo
import time
import serial
import inmoov

def setup(myInMoov):
    if not myInMoov.init('/dev/tty.usbmodemfa141', 57600):
        print ("Error initializing serial port")
        return True

    # INICIALIZAMOS CABEZA
    myInMoov.head.neck.minPos=40
    myInMoov.head.neck.restPos=50
    myInMoov.head.neck.maxPos=160
    myInMoov.head.neck.attach(12)
    myInMoov.head.neck.setSpeed(95)
    myInMoov.head.rotate.minPos=30
    myInMoov.head.rotate.restPos=130
    myInMoov.head.rotate.maxPos=150
    myInMoov.head.rotate.attach(13)
    myInMoov.head.rotate.setSpeed(90)
    myInMoov.head.jaw.minPos=10
    myInMoov.head.jaw.restPos=10
    myInMoov.head.jaw.maxPos=75
    myInMoov.head.jaw.attach(26)
    myInMoov.head.eyeX.minPos=60
    myInMoov.head.eyeX.restPos=80
    myInMoov.head.eyeX.maxPos=100
    myInMoov.head.eyeX.attach(22)
    myInMoov.head.eyeY.minPos=90
    myInMoov.head.eyeY.restPos=90
    myInMoov.head.eyeY.maxPos=100
    myInMoov.head.eyeY.attach(24)

    # INICIALIZAMOS BRAZO DERECHO
    myInMoov.rightArm.bicep.minPos=15
    myInMoov.rightArm.bicep.restPos=30
    myInMoov.rightArm.bicep.maxPos=60 # 85. ROZA CON ALGO
    myInMoov.rightArm.bicep.attach(8)
    myInMoov.rightArm.bicep.setSpeed(90)
    myInMoov.rightArm.rotate.minPos=40
    myInMoov.rightArm.rotate.restPos=90
    myInMoov.rightArm.rotate.maxPos=180
    myInMoov.rightArm.rotate.attach(9)
    myInMoov.rightArm.shoulder.minPos=0
    myInMoov.rightArm.shoulder.restPos=10
    myInMoov.rightArm.shoulder.maxPos=180
    myInMoov.rightArm.shoulder.attach(10)
    myInMoov.rightArm.omoplate.minPos=20
    myInMoov.rightArm.omoplate.restPos=20
    myInMoov.rightArm.omoplate.maxPos=70
    myInMoov.rightArm.omoplate.servoPin=11
    myInMoov.rightArm.omoplate.setSpeed(80)

    # INICIALIZAMOS MANO DERECHA
    myInMoov.rightHand.thumb.minPos=0
    myInMoov.rightHand.thumb.restPos=10
    myInMoov.rightHand.thumb.maxPos=141
    myInMoov.rightHand.thumb.attach(2)
    myInMoov.rightHand.index.minPos=0
    myInMoov.rightHand.index.restPos=20
    myInMoov.rightHand.index.maxPos=180
    myInMoov.rightHand.index.attach(3)
    myInMoov.rightHand.majeure.minPos=10
    myInMoov.rightHand.majeure.restPos=15
    myInMoov.rightHand.majeure.maxPos=180
    myInMoov.rightHand.majeure.attach(4)
    myInMoov.rightHand.ringfinger.minPos=10
    myInMoov.rightHand.ringfinger.restPos=10
    myInMoov.rightHand.ringfinger.maxPos=150
    myInMoov.rightHand.ringfinger.attach(5)
    myInMoov.rightHand.pinky.minPos=10
    myInMoov.rightHand.pinky.restPos=15
    myInMoov.rightHand.pinky.maxPos=150
    myInMoov.rightHand.pinky.attach(6)
    myInMoov.rightHand.wrist.minPos=0
    myInMoov.rightHand.wrist.restPos=10
    myInMoov.rightHand.wrist.maxPos=100
    myInMoov.rightHand.wrist.attach(7)
    myInMoov.rightHand.rest()

    myInMoov.rest()
    return True

def end(myInMoov):
    myInMoov.runTimers=False
    myInMoov.detach()
    myInMoov.saveSoundCache()