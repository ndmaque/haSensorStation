print('Boot.py loaded')

import time
#from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

import ugit
# https://raw.githubusercontent.com/ndmaque/haSensorStation/main/README.md


ssid = 'TP-Link_9162'
password = '65919675'
mqtt_server = '192.168.1.20'

client_id = ubinascii.hexlify(machine.unique_id())

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

#ugit.pull('README.md','https://raw.githubusercontent.com/ndmaque/haSensorStation/main/README.md')
#def pull_all(tree=call_trees_url,raw = raw,ignore = ignore,isconnected=False)
ugit.pull_all()

print(station.ifconfig())
