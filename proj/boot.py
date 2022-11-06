import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import dht

ssid = ''
password = ''
mqtt_server = '18.197.248.71' # HiveMQ Broker
client_id = ubinascii.hexlify(machine.unique_id())

topic_animation_sub = b'animation_TRUSP_sub'

topic_ldr_pub = b'ldr_TRUSP_pub'
topic_dht_pub = b'dht_TRUSP_pub'
topic_notif_pub = b'notif_TRUSP_pub'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
