import RPi.GPIO as GPIO
import dht11
import time
import datetime
import sys
import subprocess

command = ("python3 ../irrp.py -p -g17 -f codes air_con:on")

set_temp = 26

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin=14)

while True:
    result = instance.read()
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)

        if set_temp < result.temperature:
            subprocess.call(command.split())
        else:
            print("Command did not executed.(too low)")

        #プログラム終了
        sys.exit()
    else:
        #print("couldn't get good data")
    time.sleep(1)
