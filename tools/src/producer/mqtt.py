import json
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from src.const import MAIN_TOPIC
from src.config import MQTTConf
from src.sk import IP

load_dotenv()

BROKER_HOST = MQTTConf.HOST
WEBSOCKET_PORT = MQTTConf.PORT.WEBSOCKET


class MQTT:
    """Initial connection to MQTT broker"""
    _notification_topic = f"{MAIN_TOPIC}{IP}/notifications"

    def __init__(self) -> None:
        self._client = mqtt.Client(transport='websockets')
        self._client.connect(BROKER_HOST, WEBSOCKET_PORT, 60)
        # Subscribe notification topic first do emit notify to client
        self._client.subscribe(self._notification_topic)
        self._client.loop_start()

    ...
