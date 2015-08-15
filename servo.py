__author__ = 'Ugo'

import time

class Servo():
    def __init__(self, controller):
        self.minPos=0
        self.maxPos=180
        self.servoPin=0
        self.arduinoController=controller
        self.restPos=0
        self.currentPos=0
        self.isAttached=False

    def attach(self):
        self.isAttached=self.arduinoController.servoAttach(self.servoPin)
        return self.isAttached
        time.sleep(1)

    def detach(self):
        ok=self.arduinoController.servoDetach(self.servoPin)
        if ok:
            self.isAttached=False
        return ok
        time.sleep(1)

    def moveTo (self, pos):
        if not self.isAttached:
            print ("Servo not attached to Pin")
            return False

        if pos<self.minPos:
            pos=self.minPos
        elif pos>self.maxPos:
            pos=self.maxPos

        self.arduinoController.servoMoveTo(self.servoPin, pos)
        self.currentPos=pos

    def setSpeed (self, speed):
        if not self.isAttached:
            print ("Servo not attached to Pin")
            return False

        self.arduinoController.servoSetSpeed(self.servoPin, speed)

    def rest (self):
        if not self.isAttached:
            print ("Servo not attached to Pin")
            return False

        self.moveTo(self.restPos)






