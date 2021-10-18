import json
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from src.config import MQTTConf

load_dotenv()

BROKER_HOST = MQTTConf.HOST
WEBSOCKET_PORT = MQTTConf.PORT.WEBSOCKET


class MQTT:
    """Initial connection to MQTT broker"""

    def __init__(self) -> None:
        self._client = mqtt.Client(transport='websockets')
        self._client.connect(BROKER_HOST, WEBSOCKET_PORT, 60)
        self._client.loop_start()

    ...
