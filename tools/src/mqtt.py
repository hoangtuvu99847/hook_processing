import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from src import MQTTConf

load_dotenv()

"""
Initial connection to MQTT broker
"""
BROKER_HOST = MQTTConf.HOST
WEBSOCKET_PORT = MQTTConf.PORT.WEBSOCKET

# The callback for when a PUBLISH message is received from the server.

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def init_mqtt():
    mqtt_client = mqtt.Client(transport='websockets')
    mqtt_client.connect(BROKER_HOST, WEBSOCKET_PORT, 60)
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    mqtt_client.loop_start()
    print('Connect sucessful.')
    return mqtt_client
