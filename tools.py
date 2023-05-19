print('Boot.py V3.2 loading...')

import time
import ubinascii
import machine
import micropython
import network
import esp
import gc
import conman as con

esp.osdebug(None)
gc.collect()

ssid = 'TP-Link_9162'
password = '65919675'
mqtt_server = '192.168.1.20'
client_id = ubinascii.hexlify(machine.unique_id())

try:
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Network OK: {}'.format(station.ifconfig()))
except OSError as e:
  print("Error: Wifi Boot.py: {}".format(e))
  time.sleep(5)
  machine.reset()

try:
  mqttClient = con.connect_mqtt(client_id, mqtt_server)
except OSError as e:
  print("Error: Mqtt connection failed: {}".format(e))
  time.sleep(5)
  machine.reset()
