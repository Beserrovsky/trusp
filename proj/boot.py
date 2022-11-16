# Default libs
import time, ubinascii, machine, micropython, network, esp, gc, dht

# Mqtt lib
from umqttsimple import MQTTClient

# Proj libs
from animations import error_animation

## CONSTRAINTS

CONN_TIMEOUT = 5

esp.osdebug(None)
gc.collect()

ssid = 'Beserrinha AP'
password = 'SlowDancing123'
mqtt_server = '18.197.114.189' # HiveMQ Broker
client_id = ubinascii.hexlify(machine.unique_id())

topic_animation_sub = b'animation_TRUSP_sub'

topic_ldr_pub = b'ldr_TRUSP_pub'
topic_dht_pub = b'dht_TRUSP_pub'
topic_notif_pub = b'notif_TRUSP_pub'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

ini_time = time.time()

while station.isconnected() == False:
  if(time.time() - ini_time >= CONN_TIMEOUT) :
    error_animation("Timeout on network connection, check credentials")
    time.sleep(1)
  pass

print('Connection successful')
print(station.ifconfig())
