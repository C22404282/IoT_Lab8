from network import WLAN
import network
import umqtt.robust as umqtt
import time
from machine import Pin


wifi = WLAN(WLAN.IF_STA)
wifi.active(True)
ssid = "Sean's Galaxy S21 5G"
pw = "12345678"

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


HOSTNAME = '10.172.35.13'
PORT = 30000
TOPIC = 'temp/pico'

def callback(topic,msg):
    print(f"Recieved: {msg} for topic {topic}")
    if topic == b'temp/pico':
        msg = int.from_bytes(msg)
        if msg >= 22:
            led.on()
        else:
            led.off()
    
    
led = Pin('LED',Pin.OUT)

if not connect(wifi,ssid,pw):
    print("Couldnt connect To Wifi !")    
else:
    print("Connected to Wifi")
    
    mqtt = umqtt.MQTTClient(
        client_id =b'subscribe',
        server = HOSTNAME.encode(),
        port = PORT,
        keepalive = 7000 #secs
    )

    mqtt.connect()
    mqtt.set_callback(callback)
    mqtt.subscribe(TOPIC.encode()) 
    print(f"Subscribed to {TOPIC}")
    
    while True:
        mqtt.wait_msg()
        
