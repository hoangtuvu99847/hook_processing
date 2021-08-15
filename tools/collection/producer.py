import time
from typing import Any, Dict
from mqtt import init_mqtt
import socket
from collection.manager import ResourceManager
from collection import MAIN_TOPIC
from collection.process import Process
from collection.resources import Resource
import json
from threading import Thread


class Producer:

    def __init__(self, server_info) -> None:
        """
        Init connection to mqtt broker: 
        """
        self.server_info = server_info
        self.client = init_mqtt()
        self.resource_tool = Resource()
        self.process_tool = Process()
        self.prefix_topic = MAIN_TOPIC
        self.payload = {}

    def emit(self, manager, tp, payload) -> None:
        """
        Topic format sample:
            server/192.168.0.1/process/ram
        """
        try:
            topic = \
                f"{MAIN_TOPIC}/{self.server_info.get('ip')}/{manager}/{tp}"
            bullet = json.dumps(payload).encode('utf-8')
            infot = self.client.publish(topic, bullet)
            infot.wait_for_publish()
        except Exception as ex:
            print("EX: ", ex)

    def collect_ram(self, manager, tp) -> Dict[str, float]:
        while True:
            payload = self.resource_tool.ram()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)

    def collect_cpu(self, manager, tp) -> Dict[str, float]:
        while True:
            payload = self.resource_tool.cpu()
            self.emit(manager=manager, tp=tp, payload=payload)

    def collect_net(self, manager, tp) -> Dict[str, float]:
        while True:
            payload = self.resource_tool.net()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)

    def collect_disk(self, manager, tp) -> Dict[str, float]:
        while True:
            payload = self.resource_tool.disk()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)

    def collect_sensor(self, manager, tp) -> Dict[str, float]:
        while True:
            pass

    def produce(self) -> None:
        try:
            ram_thread = Thread(target=self.collect_ram,
                                args=('resources', 'ram'))
            cpu_thread = Thread(target=self.collect_cpu,
                                args=('resources', 'cpu'))
            net_thread = Thread(target=self.collect_net,
                                args=('resources', 'network'))
            disk_thread = Thread(target=self.collect_disk,
                                 args=('resources', 'disk'))

            cpu_thread.start()
            ram_thread.start()
            net_thread.start()
            disk_thread.start()

            cpu_thread.join()
            ram_thread.join()
            net_thread.join()
            disk_thread.join()
        except Exception as ex:
            raise

    def disconnect(self) -> None:
        pass
