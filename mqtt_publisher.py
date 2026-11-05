from network import WLAN
import network
import umqtt.robust as umqtt
import time
import mip
from machine import ADC


def connect(
    wifi_obj,
    ssid,
    pw,
    timeout=10
):
    wifi_obj.connect(ssid,pw)
    
    while timeout > 0:
        if wifi_obj.status() != 3:
            time.sleep(1)
            timeout-=1
        else:
            return True
    return False


def read_temp():
    global temp_sensor
    
    value = temp_sensor.read_u16()
    voltage = value * (3.3/2**16)
    temp = 27 - (voltage - 0.706)/ 0.001721
    return temp


temp_sensor = ADC(4)

#WIFI SETUP
wifi = WLAN(WLAN.IF_STA)
wifi.active(True)
ssid = "Sean's Galaxy S21 5G"
pw = "12345678"


#MQTT
HOSTNAME = '10.172.35.13'
PORT = 30000
TOPIC = 'temp/pico'


if not connect(wifi,ssid,pw):
    print("Couldnt connect To Wifi !")
    
else:
    mqtt = umqtt.MQTTClient(
            client_id = b'publish0',
            server = HOSTNAME.encode(),
            port = PORT,
            keepalive = 7000 #secs
    )
    mqtt.connect()
    while True:
        temp = read_temp()
        mqtt.publish(TOPIC,str(temp).encode())
        time.sleep(3)

