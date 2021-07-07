# RUN HERE
from collection_tool import CollectionTool
from dotenv import load_dotenv
import socket
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import os

load_dotenv()

LOCALHOST = os.environ.get('LOCALHOST')
BROKER_PORT = int(os.environ.get('BROKER_PORT'))
WEBSOCKET_PORT = int(os.environ.get('WEBSOCKET_PORT'))

print(LOCALHOST)
print(BROKER_PORT)
print(WEBSOCKET_PORT)


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
                    'ip': '188.188.0.0'
                })
                json_data = json.dumps(result).encode('utf-8')
                print(json_data)
                self.client.publish(self.prefix_topic + '188.188.0.0', json_data)
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
            ON CONFLICT(hostname) DO UPDATE SET ip_address = ?;
            """
            values = ("OKA", '188.188.0.0',
                      self.create_time_now(), self.create_time_now(),
                      self.ip)
            cursor.execute(sql, values)
            connection.commit()
            self.public_to_broker()
        except Exception as ex:
            print("Send -> save_information :: ", ex)
            return


if __name__ == '__main__':
    Send().save_information()
