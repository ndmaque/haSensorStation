from machine import Pin, PWM, ADC, TouchPad
import machine
import esp32
import sys,time
# not nneded see boot.py from umqttsimple import MQTTClient
from umqttsimple import MQTTClient
#import ubinascii
import ujson
#import stuff
import ugit

print('Main.py V3.1 loaded')
topic_chat = 'ha/station/chat'
topic_data = 'ha/station/data'
topic_err = 'ha/error'


last_message = 0
message_interval = 5
counter = 0

sensors = {}

touchpad = TouchPad(Pin(33))
motion = Pin(34, Pin.IN)
temp = 0
humidity = 0
daylight = ADC(Pin(32))
pot = ADC(Pin(35))
pot.atten(ADC.ATTN_11DB)

def updateSourceCode():
  pubChat("running updateSourceCode")
  files = ['boot.py', 'auth.py', 'main.py', 'ugit.py', 'umqttsimple.py']
  for file in files:
    path = 'https://raw.githubusercontent.com/ndmaque/haSensorStation/main/{}'.format(file)
    ugit.pull(file, path)
  machine.reset()
    
def sub_cb(topic, msg):
  print("Sub Callback topic={} msg={}".format(topic, msg))
  if topic == 'ha/station/cmd':
    if msg == b'PublishSensorData':
      pubSensors('topicRequestData', 'subscribed PublishSensorData request')
    elif msg == b'UpdateSourceCode':
      updateSourceCode()
  elif topic == 'ha/station/err': 
    print("Err sent ")
  
def pubChat(msg):
  client.publish(topic_chat, msg)
  
def pubSensors(triggeredBy, context):
  data = ujson.dumps(getSensors(triggeredBy, context))
  client.publish(topic_data, data)
  
def getSensors(triggeredBy, context):
  sensors['triggeredBy'] = triggeredBy
  sensors['context'] = context
  sensors['name'] = 'Hall_1'
  sensors['id'] = client_id
  sensors['time'] = time.time()
  sensors['cpuTemp'] = (esp32.raw_temperature()-32.0)/1.8
  sensors['temp'] = 0
  sensors['touchpad33'] = touchpad.read()
  sensors['humidity'] = 0
  sensors['pot'] = pot.read()
  sensors['daylight'] = daylight.read()
  sensors['motion'] = motion.value()
  return sensors

def connect_and_subscribe():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_chat)
  client.subscribe(topic_err)
  print('Connected to {}\nSubscribed to {}\nPublish to {} '.format(mqtt_server, topic_chat, topic_data))
  return client

def restart_and_reconnect():
  print('Machine Reset\nFailed to connect to MQTT broker')
  time.sleep(1)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

pubChat('Station One Booted main.py')
print('isconnected', station.isconnected())
while True:

  try:
    client.check_msg()
    if motion.value() and daylight.read() > 1800:
      print('motion =',motion.value())
      pubChat('Station One Motion Detected')
      pubSensors('motionDetected', 'test msg')
      time.sleep(3)
    
  except OSError as e:
      restart_and_reconnect()
