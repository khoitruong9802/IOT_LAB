import sys
from dotenv import load_dotenv
import os
from Adafruit_IO import MQTTClient
from Pyserial import Serial
# from AIDetect import AI
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
        self.setOnMessage(self.defaultOnMessage)
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()
        # self.client.loop_blocking()

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

    def defaultOnMessage(self, client, feed_id, payload):
        print("Nhan du lieu: " + payload + ", feed id: " + feed_id)

    def setOnMessage(self, callback):
        self.client.on_message = callback

class Main:
    def __init__(self):
        self.adafruit_mqtt = AdafruitMQTT()
        self.adafruit_mqtt.setOnMessage(self.sendCommand)
        self.ser = Serial()
        # self.ai = AI()

    def publishSensor(self, data):
        if data[1] == "T":
            self.adafruit_mqtt.publish("cambien1", data[2])
            print("Publish temp")
        elif data[1] == "L":
            self.adafruit_mqtt.publish("cambien2", data[2])
            print("Publish light")
        elif data[1] == "H":
            self.adafruit_mqtt.publish("cambien3", data[2])
            print("Publish humi")

    def publishAI(self, data):
        self.adafruit_mqtt.publish("ai", data)

    def sendCommand(self, client, feed_id, payload):
        if feed_id == "nutnhan1":
            self.ser.sendData("!" + payload + "#")
        elif feed_id == "nutnhan2":
            self.ser.sendData("!" + str(int(payload) + 2) + "#")
        print("Send command ok!")

    def run(self):
        # while True:
        #     pass
        threading.Thread(target=self.ser.run, args=(self.publishSensor,)).start()
        # threading.Thread(target=self.ai.run, args=(self.publishAI,)).start()
        
if __name__ == "__main__":
    Main().run()