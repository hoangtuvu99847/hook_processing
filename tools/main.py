# RUN HERE
from collection_tool import CollectionTool
import socket
import paho.mqtt.client as mqtt
import json
from datetime import datetime

LOCALHOST = '172.16.0.121'
BROKER_PORT = 1883
WEBSOCKET_PORT = 8000


class Send:
    def __init__(self):
        self.client = mqtt.Client(transport='websockets')
        self.tool = CollectionTool()
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.prefix_topic = 'server/'

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.ip)

    def create_time_now(self):
        return datetime.now()

    def on_message(client, userdata, msg):
        print('==> ', msg.topic+" "+str(msg.payload))

    def public_to_broker(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(LOCALHOST, WEBSOCKET_PORT, 60)
        self.client.loop_start()
        try:
            while True:
                result = CollectionTool().run()
                result.update({
                    'client': self.hostname,
                    'ip': self.ip
                })
                json_data = json.dumps(result).encode('utf-8')
                print(json_data)
                self.client.publish(self.prefix_topic + self.ip, json_data)
        except Exception as ex:
            print("Send -> public_to_broker :: ", ex)

    def save_information(self):
        import sqlite3
        try:
            connection = sqlite3.connect('../hookprocessing.db')
            cursor = connection.cursor()
            sql = """
            INSERT INTO server (hostname, ip_address, created_time, updated_time) 
            VALUES (?, ?, ?, ?)
            """
            values = (self.hostname, self.ip,
                      self.create_time_now(), self.create_time_now())
            cursor.execute(sql, values)
            connection.commit()
            self.public_to_broker()
        except Exception as ex:
            print("Send -> save_information :: ", ex)
            return


if __name__ == '__main__':
    Send().public_to_broker()
