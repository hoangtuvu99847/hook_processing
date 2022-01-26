import json
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from src.const import MAIN_TOPIC, Status
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
        self.update_connect_status()
        self._client.loop_start()

    def update_connect_status(self):
        topic = f"{MAIN_TOPIC}{IP}/status"
        status = Status.CONNECTED_STATUS  # Connected status
        gunner = self.get_client.publish(
            topic=topic, payload=json.dumps(status).encode('utf-8')
        )
        gunner.wait_for_publish()

    @property
    def get_client(self):
        return self._client

    ...
