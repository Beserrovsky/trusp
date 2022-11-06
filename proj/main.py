import machine
import time
import dht

## ! Constraints ! ####################

# default brigthness
DEFAULT_ITN = 1

## in seconds
FAST_SLEEP = 0.05
TF_SLEEP = 3

## pins
R_TOP = machine.Pin(32, machine.Pin.OUT)
R_MID = machine.Pin(33, machine.Pin.OUT)
R_BOT = machine.Pin(25, machine.Pin.OUT)
Y_TOP = machine.Pin(26, machine.Pin.OUT)
Y_MID = machine.Pin(27, machine.Pin.OUT)
Y_BOT = machine.Pin(12, machine.Pin.OUT)
G_TOP = machine.Pin(23, machine.Pin.OUT)
G_MID = machine.Pin(22, machine.Pin.OUT)
G_BOT = machine.Pin(21, machine.Pin.OUT)

sensor = dht.DHT11(machine.Pin(15))

########################################

## ! VARS ! ############################
r = [R_TOP, R_MID, R_BOT]
y = [Y_TOP, Y_MID, Y_BOT]
g = [G_TOP, G_MID, G_BOT]

itn = 3

temp = 0
hum = 0

#########################################

## ! FUNCTIONS ! ########################

def chg(arr, state, delay = None):
  for i in range(itn):
    arr[i if itn == 3 else i + 1].value(state)
    if(delay != None):
      time.sleep(delay)


def chg_all(state, delay = None):
  chg(r, state, delay)
  chg(y, state, delay)
  chg(g, state, delay)
  
def boot_animation():
  global itn
  itn = 3
  chg_all(False)
  chg_all(True, FAST_SLEEP)
  chg_all(False)
  time.sleep(10 * FAST_SLEEP)
  chg_all(True)
  time.sleep(10 * FAST_SLEEP)
  chg_all(False)


## FIXME: Callback timing inconsistent
def tf_light():
  global itn
  itn = DEFAULT_ITN
  chg(r, True)
  time.sleep(TF_SLEEP)
  chg(r, False)
  chg(g, True)
  time.sleep(TF_SLEEP)
  chg(g, False)
  chg(y, True)
  time.sleep(TF_SLEEP / 3)
  chg(y, False)

def dht_measure(verbose = False):
  global temp, hum
  sensor.measure()
  temp = sensor.temperature()
  hum = sensor.humidity()
  if (verbose):
    print("Temperatura: ")
    print(temp)
    print("Umidade: ")
    print(hum)

## def light_read():
  ## TODO

def main():
  boot_animation()
  dht_measure(True)
  while True:
    tf_light()
    dht_measure()

main()
