
import json
import threading
import signal
from src.const import MAIN_TOPIC
from src.producer.mqtt import MQTT

from src.sk import HOSTNAME, IP

exit_event = threading.Event()


def signal_handle(signum, frame):
    topic = f"{MAIN_TOPIC}disconnected"
    payload = dict(
        ip_address=IP,
        hostname=HOSTNAME
    )
    mqtt = MQTT()
    client = mqtt._client
    infot = client.publish(
        topic=topic, payload=json.dumps(payload).encode('utf-8'))
    print('::::::::: Exited Session! ::::::::::')
    infot.wait_for_publish()
    exit_event.set()


signal.signal(signal.SIGINT, signal_handle)


class CollectionThread(threading.Thread):
    def __init__(self, *args, **kwargs) -> None:
        super(CollectionThread, self).__init__(*args, **kwargs)
        self._stopevent = threading.Event()
        self._sleepperior = 1.0

    def run(self) -> None:
        return super().run()

    def join(self, timeout=None) -> None:
        """Stop the thread."""
        self._stopevent.set()
        return super().join(timeout=self._sleepperior)


if __name__ == "__main__":
    CollectionThread()
