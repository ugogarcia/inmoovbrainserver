# InMoovBrain Server
Controla tu InMoov desde tu PC

## Descripción

**InMoovBrain Server** es un aplicación hecha en Python para controlar el robot InMoov imprimible en impresoras 3D (http://www.inmoov.fr) diseñado por Gael Langevin. Se conecta al Arduino para controlar los servos y sensores conectados al mismo e integra un pequeño servidor Web que nos permite que controlemos las funciones del robot mediante una aplicación Web externa (por ejemplo [InMoovBrain Console](https://github.com/ugogarcia/inmoovbrainconsole)). Para la comunicación del servidor con el Arduino se utiliza la librería MRLComm utilizada en el proyecto [MyRobotLab](http://www.myrobotlab.org)

## Requisitos
El siguiente software es necesario para que funcione InMoovBrain Server:

* [Python 3.4.3](https://www.python.org/downloads/release/python-343/)
* [pyglet 1.2.3](https://bitbucket.org/pyglet/pyglet/wiki/Download)
* [AVbin 10](http://avbin.github.io/AVbin/Download.html)
* openssl para generar un certificado para la conexión SSL
* (opcional) Un IDE para python como [PyCharm](https://www.jetbrains.com/pycharm/download/) (o simplemente cualquier editor de texto)


## Instalación
Lo primero es tener Python 3 instalado y funcionando en tu sistema. A continuación instalar pyglet y AVbin. En el archivo _inmoovbrain.py_ se define el puerto y el nombre del host en el cual escuchará el servidor Web mediante las variable _hostPort_ y _hostName_ (por defecto localhost:8443); cambiala para adaptarla a tus necesidades.

Para que el servidor pueda atender peticiones por HTTPS hay que configurar un certificado. Para generar uno debes tener disponer de _openssl_ en tu sistema y ejecutar el siguiente comando:

```
openssl req -new -x509 -keyout localhost.pem -out localhost.pem -days 365 -nodes
```

## Configuración
Al arrancar el progrma se instancia un objeto llamado _myInMoov_ de la clase _InMoow_, Este objeto será el que se utilizará para gestionar tu robot. Antes de ejecutar el servidor Web, se llama al método _setup_ del módulo _main.py_ que debe contener la inicialización de dicho objeto, así como todas las operaciones que quieres que se ejecuten al arranque del servidor. Operaciones como inicialización del puerto serie al que está conectado el Arduino, asignación de pines a servos, definición de rango de funcionamiento de los servos, etc, son operaciones típicas que puedes incluir aqui. A continuación un ejemplo básico de inicialización del puerto serie y definición de los pines donde estarán conectados un par de servos:

```
def setup(myInMoov):
    if not myInMoov.init('/dev/tty.usbmodemfa141', 57600):
        print ("Error initializing serial port")
        return False
    myInMoov.head.neck.servoPin=12
    myInMoov.head.rotate.servoPin=13
    return True
```


## Arranque
Para arrancar el servidor basta con ejecutar el archivo _inmoovbrain.py_ ya sea desde línea de comandos o desde tu IDE favorito. 

```
MBPUgo:InMoovBrainServer Ugo$ python3 inmoovbrain.py
Running setup...
Starting server...
Server Starts - localhost:8443
```

Para probar el correcto funcionamiento del servidor basta con conectarse desde un navegador a la URL y el puerto dónde está escuchando el servidor. El servidor te devolverá una página Web de Bienvenida con una ayuda básica del uso del mismo. 


## ¿Y ahora qué?
Si tienes ya los servos conectados al arduino sólo te queda configurar [InMoovBrain Console](https://github.com/ugogarcia/inmoovbrainconsole) para poder controlar desde el interfaz Web tu InMoov.