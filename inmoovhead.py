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

    def attach(self, neckPin=None, rotatePin=None, jawPin=None, eyeXPin=None, eyeYPin=None):
        if neckPin is not None:
            self.neck.servoPin=neckPin
        if rotatePin is not None:
            self.rotate.servoPin=rotatePin
        if jawPin is not None:
            self.jaw.servoPin=jawPin
        if eyeXPin is not None:
            self.eyeX.servoPin=eyeXPin
        if eyeYPin is not None:
            self.eyeY.servoPin=eyeYPin

        self.neck.attach()
        self.rotate.attach()
        self.jaw.attach()
        self.eyeX.attach()
        self.eyeY.attach()

    def detach(self):
        self.neck.detach()
        self.rotate.detach()
        self.jaw.detach()
        self.eyeX.detach()
        self.eyeY.detach()

    def setSpeed (self, speedNeck, speedRotate, speedJaw, speedEyeX, speedEyeY):
        self.neck.setSpeed(speedNeck)
        self.rotate.setSpeed(speedRotate)
        self.jaw.setSpeed(speedJaw)
        self.eyeX.setSpeed(speedEyeX)
        self.eyeY.setSpeed(speedEyeY)

    def rest (self):
        if self.neck.servoPin!=0:
            self.neck.rest()
        if self.rotate.servoPin!=0:
            self.rotate.rest()
        if self.jaw.servoPin!=0:
            self.jaw.rest()
        if self.eyeX.servoPin!=0:
            self.eyeX.rest()
        if self.eyeY.servoPin!=0:
            self.eyeY.rest()

