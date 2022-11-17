import routines
from components import *
from animations import *

def main():
  boot_animation()
  dht_measure(True)
  light_read(True)
  reset_itn()
  while True:
    tf_light()
    dht_measure(True)
    light_read(True)
    update_itn()
    # routines.tick() # MQTT UPDATES

main()
