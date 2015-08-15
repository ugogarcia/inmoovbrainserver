__author__ = 'Ugo'
import servo

class InMoovHead():
    def __init__(self, controller):
        self.arduinoController=controller
        self.neck=servo.Servo(self.arduinoController)
        self.rotate=servo.Servo(self.arduinoController)
        self.jaw=servo.Servo(self.arduinoController)
        self.eyeX=servo.Servo(self.arduinoController)
        self.eyeY=servo.Servo(self.arduinoController)
        self.isAttached=False

    def attach(self):
        self.neck.attach()
        self.rotate.attach()
        self.jaw.attach()
        self.eyeX.attach()
        self.eyeY.attach()
        self.isAttached=True

    def detach(self):
        self.neck.detach()
        self.rotate.detach()
        self.jaw.detach()
        self.eyeX.detach()
        self.eyeY.detach()
        self.isAttached=False

    def setSpeed (self, speedNeck, speedRotate, speedJaw, speedEyeX, speedEyeY):
        self.neck.setSpeed(speedNeck)
        self.rotate.setSpeed(speedRotate)
        self.jaw.setSpeed(speedJaw)
        self.eyeX.setSpeed(speedEyeX)
        self.eyeY.setSpeed(speedEyeY)

    def rest (self):
        self.neck.rest()
        self.rotate.rest()
        self.jaw.rest()
        self.eyeX.rest()
        self.eyeY.rest()

