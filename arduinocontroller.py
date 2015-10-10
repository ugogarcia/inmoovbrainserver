__author__ = 'Ugo'
import serial
import sys
import time

MAGIC_NUMBER        = 170
SERVO_ATTACH        = 6
SERVO_ATTACH_WITH_DEFAULT        = 100
SERVO_WRITE         = 7
SERVO_DETACH        = 9
SERVO_SET_SPEED     = 12

# Mensaje ejemplo = MAGIC_NUMBER|MSG_SIZE|FUNCTION|PARAM0|PARAM2
# MSG_SIZE en bytes no incluye MAGIC_NUMBER y MSG_SIZE, solo FUNCTION y PARAMS
# Si FUNCTION es siempre un byte parece tener más sentido no incluirlo en MSG_SIZE ya que siempre estamos umando 1

# SERVO_ATTACH (1 byte) | servo index (1 byte) | servo pin (1 byte) | size of name (1 byte) | ASCII name of servo (N - bytes)
# no se usa el nombre, con lo cual podemos omitirlo. Servo index siempre es pin-2 con lo que podríamos omitirlo tb. SERVO_ATTACH|0|2

class ArduinoController:
    def __init__(self, port, baudrate):
        self.serialPort=port
        self.serialBaudrate=baudrate
        self.serialObject=None

    def initSerial(self):
        try:
            self.serialObject = serial.Serial(self.serialPort, self.serialBaudrate)
            time.sleep(2) # Es necesario una pausa para que el puerto inicialice
        except:
            print ("[ArduinoController.initSerial] " , sys.exc_info()[1])
            return False
        else:
            return True

    def writeToSerial(self, byte):
        try:
            elements=[byte]
            self.serialObject.write(bytearray(elements))
            #time.sleep(0.1)
            #print (byte)
        except:
            print ("[ArduinoController.writeToSerial] " , sys.exc_info()[1])
            return False
        else:
            return True

    def servoAttach(self, pin, default):
        # Index siempre es el pin-2. Podríamos quitar este parámetro
        if self.serialObject==None:
            print ("Serial not initialized")
            return False

        self.sendMsg(SERVO_ATTACH_WITH_DEFAULT, [pin-2, pin, default])
        print ("ATTACH Servo to Pin %d with default %d " % (pin, default))
        return True

    def servoDetach(self, pin):
        if self.serialObject==None:
            print ("Serial not initialized")
            return False

        self.sendMsg(SERVO_DETACH, [pin-2])
        print ("DETACH Servo from Pin %d" % pin)
        return True

    def servoMoveTo(self, pin, newPos):
        if self.serialObject==None:
            print ("Serial not initialized")
            return False

        self.sendMsg(SERVO_WRITE, [pin-2, newPos])
        print ("MOVE Servo Pin %d to Pos %d" % (pin, newPos))
        return True

    def servoSetSpeed(self, pin, speed):
        if self.serialObject==None:
            print ("Serial not initialized")
            return False

        self.sendMsg(SERVO_SET_SPEED, [pin-2, speed])
        print ("SETSERVOSPEED Servo Pin %d to Speed %d" % (pin, speed))
        return True

    def sendMsg(self, cmd, params):
        # Mensaje ejemplo = MAGIC_NUMBER|MSG_SIZE|FUNCTION|PARAM0|PARAM2
        # MSG_SIZE en bytes no incluye MAGIC_NUMBER y MSG_SIZE, solo FUNCTION y PARAMS
        self.writeToSerial(MAGIC_NUMBER)
        self.writeToSerial(1 + len(params))
        self.writeToSerial(cmd)
        for param in params:
            self.writeToSerial(param)