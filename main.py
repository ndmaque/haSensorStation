
from machine import Pin, PWM, ADC, TouchPad
import machine
import sys,time

#import conman as con
import tools as tool

print('Main.py 3.2 Delay: 5 Sec to crash!')
time.sleep(5)
print("continue...")

tool.pubChat(mqttClient,"Main.py test msg")
mqttClient.set_callback(tool.sub_cb)
mqttClient.subscribe('ha/station/#')

motion = Pin(34, Pin.IN)

while True:
  motionVal = motion.value()
  try:
    mqttClient.check_msg()
    if motionVal ==1:
      print('MotionTrue =', motion.value())
      tool.pubChat(mqttClient,'Station One Motion Detected')
      tool.pubSensors('motionDetected', 'test msg')
      time.sleep(15)
    else:
      print('MotionFalse=', motion.value())
      time.sleep(3)
    time.sleep(0.5)
    
  except OSError as e:
      print("Error: main.py: {}".format(e))


