import time, machine, micropython, network, esp, gc, dht, ubinascii
from umqttsimple import MQTTClient
from animations import error_animation, boot_animation

client_id = ubinascii.hexlify(machine.unique_id())

mqtt_server = '18.197.114.189' # HiveMQ Broker

topic_animation_sub = b'animation_TRUSP_sub'

topic_ldr_pub = b'ldr_TRUSP_pub'
topic_dht_pub = b'dht_TRUSP_pub'
topic_notif_pub = b'notif_TRUSP_pub'

def sub_cb(topic, msg):
  global topic_animation_sub
  print((topic, msg))
  if (topic == topic_animation_sub):
    handle_animation_sub(msg)

def handle_animation_sub(msg):
  boot_animation()

def connect_and_subscribe():
  global client_id, mqtt_server, topic_animation_sub, topic_ldr_pub, topic_dht_pub, topic_notif_pub
  client = MQTTClient(client_id, mqtt_server)

  # client.set_callback(sub_cb)

  # client.connect(topic_ldr_pub)
  # client.connect(topic_dht_pub)
  # client.connect(topic_notif_pub)

  # client.subscribe(topic_animation_sub)

  print('Connected to MQTT broker')
  return client

def restart_and_reconnect():
  error_animation("Failed to connect to MQTT broker. Reconnecting...")
  time.sleep(10)
  machine.reset()

# def handleUpdates():
#   global ldr, temp, hum
#   client.publish(topic_ldr_pub, str(ldr))
#   client.publish(topic_dht_pub, str(temp) + " : " + str(hum))

try:
  client = connect_and_subscribe()
except OSError as e:
  print(e)
  restart_and_reconnect()

def tick():
  try:
    new_message = client.check_msg()
    if new_message != None: # Handled by sub_cb
      client.publish(topic_notif_pub, b'msg received')
    # handleUpdates()
  except OSError as e:
    restart_and_reconnect()
