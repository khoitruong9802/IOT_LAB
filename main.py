import sys
import random
import time
from dotenv import load_dotenv
import os
from Adafruit_IO import MQTTClient

load_dotenv()

AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = os.getenv("AIO_USERNAME")
AIO_KEY = os.getenv("AIO_KEY")

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + ", feed id: " + feed_id)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter = 10
while True:
    counter = counter - 1
    if counter <= 0:
        counter = 10
        temp = random.randint(15, 35)
        humi = random.randint(15, 35)
        light = random.randint(15, 35)

        print("Publish sensor data.....")
        client.publish("cambien1", temp)
        client.publish("cambien2", humi)
        client.publish("cambien3", light)
    
    time.sleep(1)