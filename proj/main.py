from components import *
from animations import *

mqtt_server = '18.185.142.17' # HiveMQ Broker

ldr_pub = b'TRUSP_ldr'
dht_pub = b'TRUSP_dht'
WRN_PUB = b'TRUSP_client'

anim_sub = b'TRUSP_anim'


client_id = ubinascii.hexlify(machine.unique_id())

def connect_and_subscribe():
  global client_id, mqtt_server, anim_sub

  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()

  client.subscribe(anim_sub)

  print('Connected to MQTT broker')
  return client

def restart_and_reconnect():
  error_animation("Failed to connect to MQTT broker. Reconnecting...")
  time.sleep(10)
  machine.reset()

# Subscriptions

def sub_cb(topic, msg):
  global anim_sub
  
  print(f't: "{topic}" -> m:"{msg}"')

  if (topic == anim_sub):
    handle_animation_sub(msg)

def handle_animation_sub(msg):
  if (msg == b'boot'):
    boot_animation()


# ! IMPORTANT CALLS !

client = None

## Connects to broker
def start():
  global client, WRN_pub, client_id
  try:
    client = connect_and_subscribe()
    client.publish(WRN_PUB, f'{str(client_id.decode('utf8', 'strict'))} is up!')
  except OSError as e:
    print(e)
    restart_and_reconnect()

## Checks incoming msgs
def tick():
  try:
    new_message = client.check_msg()
    if new_message != None: # Handled by sub_cb
      print(f'Message received: {new_message}')
  except OSError as e:
    restart_and_reconnect()

## Updates sensors data
def update(ldr, temp, hum):
  global client_id

  ldrD = {
    'client_id': client_id,
    'ldr': ldr
  }

  dhtD = {
    'client_id': client_id,
    'temp': temp,
    'hum': hum
  }

  client.publish(ldr_pub, str(ujson.dumps(ldrD)))
  client.publish(dht_pub, str(ujson.dumps(dhtD)))

  print('Data sent to broker!')

# Classes

class LdrData(object):
  client_id = ""
  ldr = 0

class DhtData(object):
  client_id = ""
  temp = 0
  hum = 0


def main():
  boot_animation()
  dht_measure(True)
  light_read(True)
  reset_itn()
  while True:
    tf_light()
    ldr = light_read(True)
    temp, hum = dht_measure(True)
    update_itn()
    tick()
    update(ldr, temp, hum)

start()
main()
