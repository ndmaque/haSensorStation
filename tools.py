from machine import Pin, PWM, ADC, TouchPad
import math, time
import ubinascii
import machine
import esp32
import ujson
import ugit
from auth import AuthInfo as Auth

class Tools:

  #auth = Auth()
   
  def __init__(self):
    self.client_id = ubinascii.hexlify(machine.unique_id())
    self.touchPad = TouchPad(Pin(33))
    self.motionPin = Pin(39, Pin.IN, Pin.PULL_DOWN)
    self.daylightPin = ADC(Pin(32))
    self.thonnyKillPin = Pin(36, Pin.IN)
    self.motionLed = PWM(Pin(2), freq=1000)
    self.logs = []
    self.subPath = 'ha/station/'
    
    
  def log(self, level = 0, msg = ''):
    levels = ['Info','Warn','Fatal']
    self.logs.append("{}: | {} | {}".format(levels[level], msg, time.time()))

  def getLog(self):
    return self.logs
      
  def test(self):
    return 'client_id: {}'.format(self.client_id)
   
  def mqqtSubCB(self, topic, msg):
    topic = topic.decode()
    msg = msg.decode()
    path = self.subPath

    print("Sub Callback topic:{} msg: {} time: {}".format(topic, msg, time.time()))
    if topic == path + 'cmd/PublishSensorData':
      self.pubSensors('topicRequestData', 'subscribed PublishSensorData request')
    elif topic == path + 'cmd/UpdateSourceCode':
        self.updateSourceCode(msg)
    elif topic == path + 'cmd/RebootMachine':
        self.machine.reset()
    elif topic == path + 'error': 
      print("Err...")
    
  def pubSensors(self,mqtt, triggeredBy='', context=''):
    data = ujson.dumps(self.getSensors(triggeredBy, context))
    mqtt.publish(self.subPath +'sensor', data)

  def getSensors(self, triggeredBy ='', context = ''):
    sensors = {}
    pot = ADC(Pin(35))
    pot.atten(ADC.ATTN_11DB)
    
    sensors['triggeredBy'] = triggeredBy
    sensors['context'] = context
    sensors['name'] = 'Hall_1'
    sensors['client_id'] = self.client_id
    sensors['time'] = time.time()
    sensors['cpuTemp'] = (esp32.raw_temperature()-32.0)/1.8
    sensors['temp'] = 0
    sensors['touchpad_1'] = self.touchPad.read()
    sensors['humidity'] = 0
    sensors['pot'] = pot.read()
    sensors['daylight'] = self.daylightPin.read()
    sensors['motion'] = self.motionPin.value()
    return sensors
      
  def updateSourceCode(self, filesCsv):
    defaultFiles = 'boot.py,auth.py,main.py,ugit.py,umqttsimple.py,tools.py'

    try:
      files = filesCsv.split(',')
    except OSError as e:
      files = defaultFiles.split(',')
      self.log(2, 'updateSourceCode using defaultFiles')
        
    for file in files:
      path = 'https://raw.githubusercontent.com/ndmaque/haSensorStation/main/{}'.format(file)
      ugit.pull(file, path)
    machine.reset()
 
  def pulsePin(self, pin, speed):
    for i in range(20):
      pin.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
      time.sleep_ms(speed)
    pin.duty(0)

