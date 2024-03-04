import sys
from dotenv import load_dotenv
import os
from Adafruit_IO import MQTTClient
from Pyserial import Serial
from AIDetect import AI
import threading

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

class Main:
    def __init__(self):
        self.adafruit_mqtt = AdafruitMQTT()
        self.ser = Serial()
        self.ai = AI()

    def publishSensor(self, data):
        if data[1] == "T":
            self.adafruit_mqtt.publish("cambien1", data[2])
        elif data[1] == "L":
            self.adafruit_mqtt.publish("cambien2", data[2])
        elif data[1] == "H":
            self.adafruit_mqtt.publish("cambien3", data[2])

    def publishAI(self, data):
        self.adafruit_mqtt.publish("ai", data)

    def run(self):
        threading.Thread(target=self.ser.run, args=(self.publishSensor,)).start()
        threading.Thread(target=self.ai.run, args=(self.publishAI,)).start()
        
if __name__ == "__main__":
    Main().run()