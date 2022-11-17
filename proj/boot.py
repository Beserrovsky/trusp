# Default libs
import time, machine, micropython, network, esp, gc, dht

# Mqtt lib
from umqttsimple import MQTTClient

# Proj libs
from animations import error_animation

## CONSTRAINTS

CONN_TIMEOUT = 10

esp.osdebug(None)
gc.collect()

ssid = 'Beserrinha AP'
password = 'SlowDancing123'

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
