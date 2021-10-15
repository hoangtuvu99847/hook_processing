import time
from src.mqtt import init_mqtt
from src import MAIN_TOPIC
from src.process import Process
from src.resources import Resource
from src.db import CPU, DB, Server
from threading import Thread
import json
from src import hostname, ip


class Producer:

    def __init__(self, server_info) -> None:
        """
        Init connection to mqtt broker: 
        """
        self.server_info = server_info
        self._server_id = None
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
                id=self._server_id,
                machine=dict(
                    hostname=hostname,
                    ip_address=ip
                ))
            )
        bullet = json.dumps(payload).encode('utf-8')
        infot = self.client.publish(topic, bullet, qos=2)
        infot.wait_for_publish()

    def collect_ram(self, manager, tp):
        while True:
            payload = self.resource_tool.ram()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)

    def collect_cpu(self, manager, tp):
        while True:
            payload = self.resource_tool.cpu()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)

    def collect_net(self, manager, tp):
        while True:
            payload = self.resource_tool.net()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)

    def collect_disk(self, manager, tp):
        while True:
            payload = self.resource_tool.disk()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)

    def collect_all(self, manager, tp):
        """
        Get all resources on machine 
        """
        while True:
            payload = dict(
                machine=dict(
                    ip_address=ip,
                    hostname=hostname
                ),
                resource=dict(
                    ram=self.resource_tool.ram(),
                    cpu=self.resource_tool.cpu(),
                    disk=self.resource_tool.disk(),
                    net=self.resource_tool.net(),
                )
            )
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)

    def produce(self, server_id):
        # Save info database
        self.save_cpu_info(server_id)
        try:
            collect_all_resource_thread = Thread(target=self.collect_all,
                                                 args=('resources', '*'))
            ram_thread = Thread(target=self.collect_ram,
                                args=('resources', 'ram'))
            cpu_thread = Thread(target=self.collect_cpu,
                                args=('resources', 'cpu'))
            net_thread = Thread(target=self.collect_net,
                                args=('resources', 'network'))
            disk_thread = Thread(target=self.collect_disk,
                                 args=('resources', 'disk'))

            collect_all_resource_thread.start()
            cpu_thread.start()
            ram_thread.start()
            net_thread.start()
            disk_thread.start()

            collect_all_resource_thread.join()
            cpu_thread.join()
            ram_thread.join()
            net_thread.join()
            disk_thread.join()
        except Exception as ex:
            self.logger(type='ERROR', payload=str(ex))
            raise
        # await asyncio.gather(
        #     self.collect_all('resources', '*'),
        #     self.collect_ram('resources', 'ram'),
        #     self.collect_cpu('resources', 'cpu'),
        #     self.collect_net('resources', 'network'),
        #     self.collect_disk('resources', 'disk'),
        # )

    def save_cpu_info(self, server_id):
        """SAVE list CPU in db"""
        self._server_id = server_id
        cpu_resouce = self.resource_tool.cpu()
        if cpu_resouce:
            list_cpu = []
            for cpu in cpu_resouce.get('cpus'):
                list_cpu.append(cpu['cpu_name'])

            data_insert = ','.join(list_cpu)
            cpu_entity = CPU()
            cpu_entity.save(server_id, data_insert)

            # Commit in transaction save info server
            cpu_entity.db.commit()

    def disconnect(self) -> None:
        topic = f"{MAIN_TOPIC}disconnected"
        payload = dict(
            ip_address=ip,
            hostname=hostname
        )
        infot = self.client.publish(
            topic=topic, payload=json.dumps(payload).encode('utf-8'))
        print('::::::::: Exited Session! ::::::::::')
        infot.wait_for_publish()

    def logger(self, type='SUCCESS', payload=None):
        topic = 'logger/event'
        self.emit(tp=topic, payload=payload)
