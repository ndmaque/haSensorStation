import time, math, ujson
import ubinascii
import machine
from machine import Pin, PWM, ADC
import micropython


# Vars from boot: wlan, mqtt, auth, tool
print("Main.py v4 t={}".format(time.time()))

# TODO add a 5v power line to break Thonny bug
killPower = Pin(22, Pin.OUT, Pin.PULL_UP)
killPower.value(1)
##################

tools.pulsePin(tools.motionLed, 50)

motionAlert = 0
lastMotion = 0


def motionCb(pin):
  global motionAlert, lastMotion, mqqt, tools, daylightPin
  if tools.motionPin.value() == 1 and (time.time()-lastMotion) > 15:
    motionAlert = True
    lastMotion = time.time()
    mqtt.publish('ha/station/hall_light', ujson.dumps({'on': 1, 'daylight': tools.daylightPin.read(), 'delay':1000}))
        
tools.motionPin.irq(trigger=Pin.IRQ_RISING, handler=motionCb)

mqtt.set_callback(tools.mqqtSubCB)
mqtt.subscribe('ha/station/#')
mqtt.check_msg()
last_msg_check = time.time()

print(tools.getSytemStatus(wlan))

# main loop till kilswitch pulled for thonny can't stop
while tools.thonnyKillPin.value():
  if time.time() - last_msg_check > 5:
    last_msg_check = time.time()
    mqtt.check_msg()
  if motionAlert == 1:
    motionAlert = 0
    tools.pulsePin(tools.motionLed, 20)
  else:
    tools.motionLed.duty(0)
  time.sleep(0.1)

# end   
print("EndLoop: thonnyKillPin: {}".format(tools.thonnyKillPin.value()))
print("logs: {}".format(tools.getLog()))
