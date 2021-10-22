
import json
import threading
import signal
from src.const import MAIN_TOPIC
from src.producer.mqtt import MQTT
from src.sk import HOSTNAME, IP

exit_event = threading.Event()


def disconnect_event():
    topic = f"{MAIN_TOPIC}disconnected"
    payload = dict(
        ip_address=IP,
        hostname=HOSTNAME
    )
    mqtt = MQTT()
    client = mqtt._client
    infot = client.publish(
        topic=topic, payload=json.dumps(payload).encode('utf-8'))

    print("\n")
    print('::::::::: Terminating... ::::::::::')
    infot.wait_for_publish()


def signal_handle(signum, frame):
    """When hard quit program -> Catch event disconnect"""
    disconnect_event()
    exit_event.set()


signal.signal(signal.SIGINT, signal_handle)
