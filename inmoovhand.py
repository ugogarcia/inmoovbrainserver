__author__ = 'Ugo'
import servo
import time

class InMoovHand():
    def __init__(self, controller):
        self.arduinoController=controller
        self.thumb=servo.Servo(controller)
        self.index=servo.Servo(controller)
        self.majeure=servo.Servo(controller)
        self.ringfinger=servo.Servo(controller)
        self.pinky=servo.Servo(controller)
        self.wrist=servo.Servo(controller)

    def attach(self, thumbPin=None, indexPin=None, majeurePin=None, ringfingerPin=None, pinkyPin=None, wristPin=None):
        if thumbPin is not None:
            self.thumb.servoPin=thumbPin
        if indexPin is not None:
            self.index.servoPin=indexPin
        if majeurePin is not None:
            self.majeure.servoPin=majeurePin
        if ringfingerPin is not None:
            self.ringfinger.servoPin=ringfingerPin
        if pinkyPin is not None:
            self.pinky.servoPin=pinkyPin
        if wristPin is not None:
            self.wrist.servoPin=wristPin

        self.thumb.attach()
        self.index.attach()
        self.majeure.attach()
        self.ringfinger.attach()
        self.pinky.attach()
        self.wrist.attach()

    def detach(self):
        self.thumb.detach()
        self.index.detach()
        self.majeure.detach()
        self.ringfinger.detach()
        self.pinky.detach()
        self.wrist.detach()

    def setSpeed (self, speedThumb, speedIndex, speedMajeure, speedRingFinger, speedPinky, speedWrist):
        self.thumb.setSpeed(speedThumb)
        self.index.setSpeed(speedIndex)
        self.majeure.setSpeed(speedMajeure)
        self.ringfinger.setSpeed(speedRingFinger)
        self.pinky.setSpeed(speedPinky)
        self.wrist.setSpeed(speedWrist)

    def moveTo (self, posThumb=None, posIndex=None, posMajeure=None, posRingFinger=None, posPinky=None, posWrist=None):
        self.thumb.moveTo(posThumb)
        self.index.moveTo(posIndex)
        self.majeure.moveTo(posMajeure)
        self.ringfinger.moveTo(posRingFinger)
        self.pinky.moveTo(posPinky)
        self.wrist.moveTo(posWrist)

    def setAutoDetachTime(self, detachTime):
        self.thumb.autoDetachTime=detachTime
        self.index.autoDetachTime=detachTime
        self.majeure.autoDetachTime=detachTime
        self.ringfinger.autoDetachTime=detachTime
        self.pinky.autoDetachTime=detachTime
        self.wrist.autoDetachTime=detachTime

    def rest (self):
        self.thumb.rest()
        self.index.rest()
        self.majeure.rest()
        self.ringfinger.rest()
        self.pinky.rest()
        self.wrist.rest()

    def open(self):
        self.moveTo(0)
        time.sleep(0.4)
        self.moveTo(None,0,0,0,0)

    def close(self):
        self.moveTo(None,180,180,180,180)
        time.sleep(0.4)
        self.moveTo(180)



