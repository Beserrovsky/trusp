import machine, dht

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
ldr = machine.ADC(machine.Pin(34))

########################################

## ! VARS ! ############################
r = [R_TOP, R_MID, R_BOT]
y = [Y_TOP, Y_MID, Y_BOT]
g = [G_TOP, G_MID, G_BOT]

itn = 3

lig = 0
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

def light_read(verbose = False):
  global lig
  lig = ldr.read_u16() 
  if (verbose):
    print("Luminosidade: ")
    print(lig)

def update_itn():
  global itn, lig
  if (lig < 10000):
    itn = 1
  elif (lig < 50000):
    itn = 2
  else:
    itn = 3
  
  chg_all(False)

def reset_itn():
  global itn
  itn = DEFAULT_ITN
