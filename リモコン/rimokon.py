import paho.mqtt.client as mqtt
import subprocess
import json
from time import sleep

HOST = 'mqtt.beebotte.com'
PORT = 8883
CA_CERTS = 'mqtt.beebotte.com.pem'
# TOKEN = '[  ]'  
# TOPIC = '[]'  

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
    data = json.loads(msg.payload.decode("utf-8"))["data"][0]
    print(msg.payload.decode("utf-8"))
    print(data)

    def default_command(data):
        subprocess.call(["python3", "irrp.py", "-p", "-g17", "-f", "codes", data["device"]+":"+data["action"]])
        print("excuted command: " + data["device"]+":"+data["action"])
        print(" ")

    # control ps4
    if (data["device"] == 'ps4'):
        subprocess.call(["python3","L_tika.py"])  
        if (data["action"] == 'on'):
            subprocess.call(["sudo", "/opt/nodejs/bin/ps4-waker"])
        elif (data["action"] == 'standby'):
            subprocess.call(["sudo", "/opt/nodejs/bin/ps4-waker", "standby"])
        elif (data["action"] == 'enter'):
            subprocess.call(["sudo", "/opt/nodejs/bin/ps4-waker", "remote", "enter"])
        elif (data["action"] == 'back'):
            subprocess.call(["sudo", "/opt/nodejs/bin/ps4-waker", "remote", "back"])
        elif (data["action"] == 'torne'):
            subprocess.call(["sudo", "/opt/nodejs/bin/ps4-waker", "start", "CUSA00442"])
        elif (data["action"] == 'primevideo'):
            subprocess.call(["sudo", "/opt/nodejs/bin/ps4-waker", "start", "CUSA03099"])
        elif (data["action"] == 'youtube'):
            subprocess.call(["sudo", "/opt/nodejs/bin/ps4-waker", "start", "CUSA01065"])
        print(" ")

    # control by temperature
    elif (data["device"] == 'temp'):
        subprocess.call(["cd", "DHT11_Python"])
        subprocess.call(["python3", "dht11_for_homeauto.py"])
        subprocess.call(["cd", ".."])
        print(" ")

    # control other
    else:
        default_command(data)
        print(" ")

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('token:%s' % TOKEN)
    client.tls_set(CA_CERTS)
    client.connect(HOST, PORT)
    client.subscribe(TOPIC)
    client.loop_forever()
