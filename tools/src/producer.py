import time
import asyncio
from typing import Any, Dict
from src.mqtt import init_mqtt
from src import MAIN_TOPIC
from src.process import Process
from src.resources import Resource
import json
from threading import Thread
from src import hostname, ip


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

    def emit(self, manager=None, tp="", payload={}) -> None:
        """
        Topic format sample:
            server/192.168.0.1/process/ram
        """
        topic = f"{self.prefix_topic}{self.server_info.get('ip')}/{manager}/{tp}"
        if payload:
            payload.update(dict(
                machine=dict(
                    hostname=hostname,
                    ip_address=ip
                ))
            )
        bullet = json.dumps(payload).encode('utf-8')
        infot = self.client.publish(topic, bullet)
        infot.wait_for_publish()

    async def collect_ram(self, manager, tp):
        while True:
            payload = self.resource_tool.ram()
            self.emit(manager=manager, tp=tp, payload=payload)
            await asyncio.sleep(1)

    async def collect_cpu(self, manager, tp):
        while True:
            payload = self.resource_tool.cpu()
            self.emit(manager=manager, tp=tp, payload=payload)
            await asyncio.sleep(1)

    async def collect_net(self, manager, tp):
        while True:
            payload = self.resource_tool.net()
            self.emit(manager=manager, tp=tp, payload=payload)
            await asyncio.sleep(1)

    async def collect_disk(self, manager, tp):
        while True:
            payload = self.resource_tool.disk()
            self.emit(manager=manager, tp=tp, payload=payload)
            await asyncio.sleep(1)

    async def collect_sensor(self, manager, tp):
        while True:
            payload = self.resource_tool.sensor()
            self.emit(manager=manager, tp=tp, payload=payload)
            await asyncio.sleep(1)

    async def produce(self):
        await asyncio.gather(
            self.collect_ram('resource', 'ram'),
            self.collect_cpu('resource', 'cpu'),
            self.collect_net('resource', 'network'),
            self.collect_disk('resource', 'disk'),
            self.collect_sensor('resource', 'sensor'),
        )

    def disconnect(self) -> None:
        topic = f"{MAIN_TOPIC}disconnected"
        payload = self.server_info.get('ip')
        infot = self.client.publish(
            topic=topic, payload=json.dumps(payload).encode('utf-8'))
        print('::::::::: Exited Session! ::::::::::')
        infot.wait_for_publish()

    def logger(self, type='SUCCESS', payload=None):
        topic = 'logger/event'
        self.emit(tp=topic, payload=payload)
