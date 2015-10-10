__author__ = 'Ugo'

import time

class Servo():
    def __init__(self, controller):
        self.minPos=0
        self.maxPos=180
        self.servoPin=0
        self.arduinoController=controller
        self.restPos=90
        self.currentPos=0
        self.isAttached=False
        self.autoDetachTime=3
        self.lastMoveTime=0

    def attach(self, pin=None, defaultPos=None):
        if pin is not None:
            self.servoPin=pin
        if self.servoPin==0:
            return False
        if defaultPos is None:
            defaultPos=self.restPos

        self.arduinoController.servoAttach(self.servoPin, defaultPos)
        self.isAttached=True
        self.lastMoveTime=time.time()
        self.currentPos=defaultPos
        return self.isAttached

    def detach(self):
        if self.servoPin==0:
            return False

        self.arduinoController.servoDetach(self.servoPin)
        self.isAttached=False
        self.lastMoveTime=time.time()
        return self.isAttached

    def moveTo (self, pos, forceAttach=True):
        if pos is None:
            return True

        if pos<self.minPos:
            pos=self.minPos
        elif pos>self.maxPos:
            pos=self.maxPos

        if self.servoPin==0:
            print ("Servo not attached to Pin")
            return False

        if forceAttach==True and self.isAttached==False:
            self.attach(self.servoPin, pos)
        elif forceAttach==False:
            print ("Servo not attached to Pin")
            return False

        self.arduinoController.servoMoveTo(self.servoPin, pos)
        self.lastMoveTime=time.time()
        self.currentPos=pos
        return True

    def setSpeed (self, speed):
        if self.servoPin!=0:
            self.arduinoController.servoSetSpeed(self.servoPin, speed)
            self.lastMoveTime=time.time()
        else:
            print ("Servo not attached to Pin")

    def rest (self, forceAttach=True):
        self.moveTo(self.restPos, forceAttach)






