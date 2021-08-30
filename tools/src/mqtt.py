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


def init_mqtt():
    mqtt_client = mqtt.Client(transport='websockets')
    mqtt_client.connect(BROKER_HOST, WEBSOCKET_PORT, 60)
    mqtt_client.loop_start()
    print('Connect sucessful.')
    return mqtt_client
