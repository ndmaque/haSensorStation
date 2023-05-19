from umqttsimple import MQTTClient


def connect_mqtt(client_id, mqtt_server):
  client = {}
  try:
    client = MQTTClient(client_id, mqtt_server)
    client.connect()
  except OSError as e:
    print("Mqtt failed to connect")
  return client