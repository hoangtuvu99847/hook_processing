import os
import socket
import time
from collection.manager import ResourceManager
from collection import MAIN_TOPIC
from collection.process import Process
from collection.resources import Resource
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import json

load_dotenv()

LOCALHOST = os.environ.get('LOCALHOST')
BROKER_PORT = int(os.environ.get('BROKER_PORT'))
WEBSOCKET_PORT = int(os.environ.get('WEBSOCKET_PORT'))


class Producer:
    def __init__(self) -> None:
        self.client = mqtt.Client(transport='websockets')
        self.resource_tool = Resource()
        self.process_tool = Process()
        self.info = {
            'user': {
                'hostname': socket.gethostname(),
                'ip': socket.gethostbyname(socket.gethostname())
            }
        }
        self.prefix_topic = MAIN_TOPIC
        self.payload = {}

    def on_connect(self, client, userdata, flags, rc) -> None:
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg) -> None:
        print('==> ', msg.topic+" "+str(msg.payload))

    def on_disconnect(self, client, userdata, rc) -> None:
        if rc != 0:
            print("BROKER DISCONNECT!!!!!.")

    def init_mqtt(self) -> None:
        try:
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            self.client.connect(LOCALHOST, WEBSOCKET_PORT, 60)
            self.client.loop_start()
        except Exception as ex:
            pass

    def produce(self):
        self.init_mqtt()
        pass

    def emit(self, manager, tp, payload):
        """
        Topic format sample:
            server/192.168.0.1/process/ram
        """
        try:
            topic = \
                f"{MAIN_TOPIC}/{self.info['user'].get('ip')}/{manager}/{tp}"
            bullet = json.dumps(payload).encode('utf-8')
            infot = self.client.publish(topic, bullet)
            infot.wait_for_publish()
            print("==>: ",  bullet)
        except Exception as ex:
            print("EX: ", ex)

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


class RAMPublisher(Producer, ResourceManager):
    def __init__(self) -> None:
        super().__init__()
        self.topic = "ram"

    def produce(self):
        self.init_mqtt()
        try:
            while True:
                payload = Resource.ram()
                payload.update(self.info)
                # Emit to broker:
                self.emit(manager=self.manage,
                          tp=self.topic, payload=payload)
                time.sleep(1)
                print(payload)
        except Exception as ex:
            print("RAMPublisher ->  produce:: ", ex)


class CPUPublisher(Producer):
    def __init__(self) -> None:
        super().__init__()

    def produce(self):
        self.init_mqtt()
        try:
            while True:
                payload = Resource.ram()
                payload.update(self.info)
                # Emit to broker:
                self.emit(manager=self.manage,
                          tp=self.topic, payload=payload)
        except Exception as ex:
            print("CPUPublisher ->  produce:: ", ex)


class NetworkPublisher(Producer):
    def __init__(self) -> None:
        super().__init__()

    def produce(self):
        self.init_mqtt()
        try:
            while True:
                payload = Resource.net()
                payload.update(self.info)
                # Emit to broker:
                self.emit(manager=self.manage,
                          tp=self.topic, payload=payload)
        except Exception as ex:
            print("NetworkPublisher ->  produce:: ", ex)


class SensorPublisher(Producer):
    def __init__(self) -> None:
        super().__init__()

    def produce(self):
        self.init_mqtt()
        try:
            while True:
                payload = Resource.sensor()
                payload.update(self.info)
                # Emit to broker:
                self.emit(manager=self.manage,
                          tp=self.topic, payload=payload)
        except Exception as ex:
            print("SensorPublisher ->  produce:: ", ex)


