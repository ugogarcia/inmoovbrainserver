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
    myInMoov.head.neck.servoPin=12
    myInMoov.head.rotate.servoPin=13



    #myInMoov.head.attach()
    #myInMoov.rest()
    #myInMoov.rightHand.setSpeed(100,100,100,100,100,100)
    #myInMoov.rightHand.thumb.moveTo(0)
    #myInMoov.rightHand.index.moveTo(0)
    #time.sleep(100)
    #myInMoov.rightHand.thumb.moveTo(180)
    #myInMoov.rightHand.index.moveTo(180)
    #time.sleep(10)
    #myInMoov.rightHand.thumb.moveTo(90)
    #myInMoov.rightHand.index.moveTo(90)
    #time.sleep(5)
    #myInMoov.rightHand.thumb.detach()
    #myInMoov.rightHand.index.detach()


    #arduinoController=arduinocontroller.ArduinoController('/dev/tty.usbmodemfa141', 57600)
    #if not arduinoController.initSerial():
    #    print ("Error initializing serial port")
    #    return False
    #testServo=servo.Servo(arduinoController)
    #testServo.attach(13)
    #testServo.setSpeed(100)
    #testServo.moveTo(90)
    #time.sleep(3)
    return True
