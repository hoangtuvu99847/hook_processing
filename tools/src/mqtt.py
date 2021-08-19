import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from src import cfg

load_dotenv()

"""
Initial connection to MQTT broker
"""
# mqtt:
#   tcp: 1883
#   websocket: 8000
#   broker: 8080
BROKER_HOST = cfg['mqtt']['host']
WEBSOCKET_PORT = cfg['mqtt']['port']['websocket']


def init_mqtt():
    mqtt_client = mqtt.Client(transport='websockets')
    mqtt_client.connect(BROKER_HOST, WEBSOCKET_PORT, 60)
    mqtt_client.loop_start()
    print('Connect sucessful.')
    return mqtt_client
