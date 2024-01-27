import sys
import random
import time
from dotenv import load_dotenv
import os
from Adafruit_IO import MQTTClient

class AdafruitMQTT:

    def __init__(self):

        if load_dotenv():
            self.AIO_FEED_IDS = ["nutnhan1", "nutnhan2"]
            self.AIO_USERNAME = os.getenv("AIO_USERNAME")
            self.AIO_KEY = os.getenv("AIO_KEY")
        else:
            print("Fail to read from env")
            sys.exit(1)

        self.client = MQTTClient(self.AIO_USERNAME , self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()

    def connected(self, client):
        print("Ket noi thanh cong ...")
        for topic in self.AIO_FEED_IDS:
            client.subscribe(topic)
            
    def publish(self, feed_id, value, group_id = None, feed_user = None):
        self.client.publish(feed_id, value, group_id, feed_user)

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribe thanh cong ...")

    def disconnected(self, client):
        print("Ngat ket noi ...")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        print("Nhan du lieu: " + payload + ", feed id: " + feed_id)

if __name__ == "__main__":
    adafruit_mqtt = AdafruitMQTT()

    counter = 10
    while True:
        counter = counter - 1
        if counter <= 0:
            counter = 10
            temp = random.randint(15, 35)
            humi = random.randint(15, 35)
            light = random.randint(15, 35)

            print("Publish sensor 1 data.....")
            adafruit_mqtt.publish("cambien1", temp)
            print("Publish sensor 2 data.....")
            adafruit_mqtt.publish("cambien2", humi)
            print("Publish sensor 3 data.....")
            adafruit_mqtt.publish("cambien3", light)
        
        time.sleep(1)