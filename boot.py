import machine
import network
import time
import gc
import ujson

from umqttsimple import MQTTClient
from auth import AuthInfo as Auth
from tools import Tools

gc.collect()
auth = Auth()
tools = Tools()

tools.log(0, "Boot.py v4")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
try:
  wlan.connect(auth.wifi['ssid'], auth.wifi['pass'])
  while wlan.isconnected() == False:
    pass
  tools.log(0, "RSSI | {}".format(wlan.status('rssi')))
  tools.log(0, "IP | {}".format(wlan.ifconfig()[0]))
except OSError as e:
  tools.log(2, 'wlan.connect | {}'.format(e))

mqtt = MQTTClient(auth.client_id, auth.mqtt['ip'])
try:
  mqtt.connect()
except OSError as e:
  tools.log(2, 'mqtt.connect | {}'.format(e))


mqtt.publish('ha/station/bootLog', ujson.dumps(tools.getLog()))
