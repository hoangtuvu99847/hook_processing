import os
from pprint import pprint
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv()

"""
Initial connection to MQTT broker
"""


def init_mqtt():
    mqtt_client = mqtt.Client(transport='websockets')
    mqtt_client.connect(os.environ.get('LOCALHOST'), int(
        os.environ.get('WEBSOCKET_PORT')), 60)
    mqtt_client.loop_start()
    print('Connect sucessful.')
    print('If you want to quit. Press Ctrl + C.')
    return mqtt_client
