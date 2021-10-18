import json
import paho.mqtt.subscribe as subscribe
from src import MAIN_TOPIC
from src.config import MQTTConf

KILL_PROCESS = 'kill'


class HandleAction:
    """Class dispatch action received"""

    def __init__(self) -> None:
        pass

    def kill_process(self, process):
        print('Kill process')


class Observe:
    """Listenter action sent from process action on client"""

    def handle(self, message):
        handler = HandleAction()
        action = message.get('action')
        if action['type'] == KILL_PROCESS:
            handler.kill_process(None)
        elif ...:
            ...

    def on_message(self, client, userdata, message):
        message = json.loads(message.payload.decode('ascii'))
        self.handle(message)

    def callback(self, topic):
        """Consume message received from another client
            Topic format sample:
            server/192.168.0.1/actions
        """

        topic = f"{MAIN_TOPIC}{topic}/actions"
        print(topic)
        subscribe.callback(self.on_message, topic, hostname=MQTTConf.HOST)
