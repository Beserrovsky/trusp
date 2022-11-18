# TRUSP

IOT device for simulating a traffic light with MQTT communication.

## Structure

This project consists in a client (ESP-32 running micropython firmware) and a server wrapped with nodeJs and MongoDB.

In order to launch the project follow:

[Client Install](README.md#Client-Install) for circuit and client code.
[Server Install](README.md#Server-Install) for database and server deployment.

## Client features

The client (device), has some features, such as:

- Animations
- DHT11 data collection and publish
- LDR data collection, publish and variance on luminous intensity
- Three-way traffic light with LEDs in parallel
- Support for 9V batterry

TODO: ADD PHOTOS

## Server and database features

For saving the data sent to broker run the server nodejs app or the dockerized container, features:

- Saving any topics listed in array to database
- Database exposure for remote access and data analysis

**TODO: ADD CHARTS AND PRINTS**

## Client Install

In order to use this project:

1. Create circuit

Follow the schematics or the photos of the device and create the circuit in a protoboard, pcb, or anything really;

2. Upload micropython firmware

As stated in [micropython.md](micropython.md), get micropython firmware from:

[ESP32](https://micropython.org/download/esp32/)
[ESP8266](https://micropython.org/download/esp8266-1m/)

`sudo pip3 install esptool`
> Install esptool

Then, upload it to the microcontroler: (Often pressing the reset pin is necessarry)

`esptool.py --port /dev/ttyUSB0 erase_flash`
> Erase old firm

`esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 YOUR_FIRMWARE.bin`
> Flash new firm, replace YOUR_FIRMWARE.bin to the correct archive name

3. Change WIFI credentials and mqtt topics

Firstly, if you haven't already, clone this repository:

`git clone https://github.com/Beserrovsky/trusp`

`cd ./trusp/client`
> Go to client dir

`vim boot.py`
> Use your text-editor to change the SSID and password fields

`vim main.py`
> Use your text-editor to change:

mqtt_server: To ip address of your broker
ldr_pub: To an unique topic for your light resistence data
dht_pub: To an unique topic for your temperature and humidity data
WRN_PUB: To an unique topic for your client status data
anim_sub: To an unique topic for your animation triggering subscription

4. Upload client code

`sudo pip3 install adafruit-ampy`
> Install ampy

`bash put.sh`
> Upload scripts -> This often fails, so try it again and again, pressing the boot reset button

5. Test code connecting to device

`sudo apt-get update`
`sudo apt-get install picocom`
> Install picocom

`picocom -b 115200 /dev/ttyUSB0`
> Connect to REPL terminal

Important:
**REMEMBER TO PRESS BOOT BUTTON TO UPDATE CODE EXECUTION**

6. Check MQTT data

If you are using something like HiveMQ public broker, you can access the data by the websocket client to check if erverything is working as intended.

## Server Install

TODO
