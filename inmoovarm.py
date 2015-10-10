__author__ = 'Ugo'
import servo

class InMoovArm():
    def __init__(self, controller):
        self.arduinoController=controller
        self.omoplate=servo.Servo(self.arduinoController)
        self.shoulder=servo.Servo(self.arduinoController)
        self.rotate=servo.Servo(self.arduinoController)
        self.bicep=servo.Servo(self.arduinoController)
        self.isAttached=False

    def attach(self, bicepPin=None, rotatePin=None, shoulderPin=None, omoplatePin=None):
        if omoplatePin!=None:
            self.omoplate.servoPin=omoplatePin
        if shoulderPin!=None:
            self.shoulder.servoPin=shoulderPin
        if rotatePin!=None:
            self.rotate.servoPin=rotatePin
        if bicepPin!=None:
            self.bicep.servoPin=bicepPin

        self.omoplate.attach()
        self.shoulder.attach()
        self.rotate.attach()
        self.bicep.attach()
        self.isAttached=True

    def detach(self):
        self.omoplate.detach()
        self.shoulder.detach()
        self.rotate.detach()
        self.bicep.detach()
        self.isAttached=False

    def setSpeed (self, speedOmoplate, speedShoulder, speedRotate, speedBicep):
        self.omoplate.setSpeed(speedOmoplate)
        self.shoulder.setSpeed(speedShoulder)
        self.rotate.setSpeed(speedRotate)
        self.bicep.setSpeed(speedBicep)

    def rest (self):
        self.omoplate.rest()
        self.shoulder.rest()
        self.rotate.rest()
        self.bicep.rest()

