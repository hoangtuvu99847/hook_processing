import json
import paho.mqtt.subscribe as subscribe
from src.const import ACTION_PROCESS, MAIN_TOPIC, STATUS_KILL_PROCESS
from src.config import MQTTConf
import os
import signal
from src.producer.mqtt import MQTT
from src.sk import IP
from src.signal.event import exit_event


class HandleAction:
    """Class dispatch action received"""

    def __init__(self) -> None:
        self._notification_topic = f"{MAIN_TOPIC}{IP}/notifications"

    def notification(self):
        """When process execute succesful -> Send notification opposite client"""
        mqtt = MQTT()
        # Get client instance
        client = mqtt.get_client
        message = {"code": STATUS_KILL_PROCESS.END_PROCESS_SUCCESS}
        bullet = json.dumps(message).encode('utf-8')
        client.publish(self._notification_topic, bullet)

    def kill_process(self, pid):
        try:
            os.kill(pid, signal.SIGKILL)  # Terminate process (NOT kill)
            self.notification()
        except Exception as ex:
            pass

    def terminate_process(self, pid):
        try:
            os.kill(pid, signal.SIGTERM)  # Terminate process (NOT kill)
            self.notification()
        except Exception as ex:
            pass


class Observe:
    """Listenter action sent from process action on client
    Example message: 
    """

    @staticmethod
    def handle(message):
        handler = HandleAction()
        if message['type'] == ACTION_PROCESS.KILL:
            handler.kill_process(message.get('pid'))
        elif message['type'] == ACTION_PROCESS.TERMINATE:
            handler.terminate_process(message.get('pid'))
        else:
            pass

    def on_message(self, client, userdata, message):
        message = json.loads(message.payload.decode('ascii'))
        self.handle(message)

    def callback(self, topic):
        """Consume message received from another client
            Topic format sample:
            server/192.168.0.1/actions
        """

        topic = f"{MAIN_TOPIC}{topic}/actions"
        subscribe.callback(self.on_message, topic, hostname=MQTTConf.HOST)


class Logger:
    def warning(self, msg):
        pass

    def danger(self, msg):
        pass


if __name__ == "__main__":
    Observe().callback('abc')
