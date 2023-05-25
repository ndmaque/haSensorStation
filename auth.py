import ubinascii
import machine

class AuthInfo:
  def __init__(self):
    self.wifi = {'ssid': 'VM6183911', 'pass':'ST*ting2436'}
    self.mqtt = {'ip':'192.168.0.20', 'pass': ''}
    self.client_id = ubinascii.hexlify(machine.unique_id())

  def test(self):
    return 'client_id: {}'.format(self.client_id)