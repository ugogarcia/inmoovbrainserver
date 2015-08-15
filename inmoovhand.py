__author__ = 'Ugo'
import servo

class InMoovHand():
    def __init__(self, controller):
        self.arduinoController=controller
        self.thumb=servo.Servo(controller)
        self.index=servo.Servo(controller)
        self.majeure=servo.Servo(controller)
        self.ringfinger=servo.Servo(controller)
        self.pinky=servo.Servo(controller)
        self.wrist=servo.Servo(controller)
        self.isAttached=False

    def attach(self):
        self.thumb.attach()
        self.index.attach()
        self.majeure.attach()
        self.ringfinger.attach()
        self.pinky.attach()
        self.wrist.attach()
        self.isAttached=True

    def detach(self):
        self.thumb.detach()
        self.index.detach()
        self.majeure.detach()
        self.ringfinger.detach()
        self.pinky.detach()
        self.wrist.detach()
        self.isAttached=False

    def setSpeed (self, speedThumb, speedIndex, speedMajeure, speedRingFinger, speedPinky, speedWrist):
        self.thumb.setSpeed(speedThumb)
        self.index.setSpeed(speedIndex)
        self.majeure.setSpeed(speedMajeure)
        self.ringfinger.setSpeed(speedRingFinger)
        self.pinky.setSpeed(speedPinky)
        self.wrist.setSpeed(speedWrist)

    def rest (self):
        self.thumb.rest()
        self.index.rest()
        self.majeure.rest()
        self.ringfinger.rest()
        self.pinky.rest()
        self.wrist.rest()



