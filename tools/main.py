# RUN HERE
import sys
from time import sleep
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


class Send:
    def __init__(self):
        self.client = mqtt.Client(transport='websockets')
        self.tool = CollectionTool()
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        # self.hostname = 'hosttest'
        # self.ip = '122.1333.1333'
        self.prefix_topic = 'server/'
        self.payload = {}

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.ip)

    def create_time_now(self):
        return datetime.now()

    def on_message(self, client, userdata, msg):
        print('==> ', msg.topic+" "+str(msg.payload))

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("BROKER DISCONNECT!!!!!.")

    def public_to_broker(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(LOCALHOST, WEBSOCKET_PORT, 60)
        self.client.loop_start()
        try:
            while True:
                result = CollectionTool().run()
                result.update({
                    'client': self.hostname,
                    'ip': self.ip
                })
                self.payload = json.dumps(result).encode('utf-8')
                print(self.payload)
                self.client.publish(self.prefix_topic + self.ip, self.payload)
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
            values = (self.hostname, self.ip,
                      self.create_time_now(), self.create_time_now(),
                      self.ip)
            cursor.execute(sql, values)
            connection.commit()
            self.public_to_broker()
        except Exception as ex:
            print("===>>> Send -> save_information :: ", ex)
            return


if __name__ == '__main__':
    s = Send()
    try:
        s.save_information()
    except KeyboardInterrupt:
        print('Interrupted')
        s.payload = {'server': s.ip}
        data = json.dumps(s.payload).encode('utf-8')
        s.client.publish('disconnect_server', data)
        sleep(3)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

