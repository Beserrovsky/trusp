import time

from components import *

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
  chg(r, True)
  time.sleep(TF_SLEEP)
  chg(r, False)
  chg(g, True)
  time.sleep(TF_SLEEP)
  chg(g, False)
  chg(y, True)
  time.sleep(TF_SLEEP / 3)
  chg(y, False)

def error_animation(msg):
  print(msg)
  chg_all(True)
  time.sleep(1)
  chg_all(False)
  time.sleep(0.5)
