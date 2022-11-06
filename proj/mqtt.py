def sub_cb(topic, msg):
  global topic_animation_sub
  print((topic, msg))
  if (topic == topic_animation_sub):
    handle_animation_sub(msg)

def handle_animation_sub(msg):
  boot_animation()

def connect_and_subscribe():
  global topic_animation_sub, topic_ldr_pub, topic_dht_pub, topic_notif_pub
  client = MQTTClient(client_id, mqtt_server)

  client.set_callback(sub_cb)

  client.connect(topic_ldr_pub)
  client.connect(topic_dht_pub)
  client.connect(topic_notif_pub)

  client.subscribe(topic_animation_sub)

  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_led_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def handleUpdates():
  global ldr, temp, hum
  client.publish(topic_ldr_pub, str(ldr))
  client.publish(topic_dht_pub, str(temp) + " : " + str(hum))

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

def tick():
  try:
    new_message = client.check_msg()
    if new_message != None: # Handled by sub_cb
      client.publish(topic_notif_pub, b'msg received')
    handleUpdates()
  except OSError as e:
    restart_and_reconnect()
