import time
from src.const import MAIN_TOPIC, DATETIME_FORMAT
from src.producer.mqtt import MQTT
from src.collector.resources.resources import Resource
from src.collector.process.process import Process
from src.db.models import CPU
from threading import Thread
import json
from datetime import datetime

from src.signal.event import exit_event


class CollectorEmitter:
    """Class initial connection machine with MQTT broker"""

    # Try connect MQTT broker
    try:
        mqtt = MQTT()
        # Get client instance
        client = mqtt.get_client
    except Exception as ex:
        raise

    def __init__(self, server_info) -> None:
        self.server_info = server_info
        self._server_id = None
        self.prefix_topic = MAIN_TOPIC
        self.payload = {}

    def emit(self, manager=None, tp="", payload=None, is_global=False) -> None:
        """
        Topic format sample:
            server/192.168.0.1/process/ram
        """
        if not is_global:
            topic = f"{self.prefix_topic}{self.server_info.get('ip')}/{manager}/{tp}"
        else:
            topic = f"{manager}/{tp}"
        if payload:
            payload.update(dict(
                id=self._server_id,
                machine=dict(
                    hostname=self.server_info.get('hostname'),
                    ip_address=self.server_info.get('ip')
                ))
            )
        bullet = json.dumps(payload).encode('utf-8')
        infot = self.client.publish(topic, bullet)
        infot.wait_for_publish()

    def logger(self, type='SUCCESS', payload=None):
        topic = 'logger/event'
        self.emit(tp=topic, payload=payload)


class ResourcesEmitter(CollectorEmitter):
    def __init__(self, server_info) -> None:
        super().__init__(server_info)

    def produce(self, manager, tp, callback):
        while True:
            self.emit(manager=manager, tp=tp, payload=callback)
            time.sleep(1)

    def collect_ram(self, manager, tp):
        while True:
            payload = Resource().ram()
            percent = payload.get('percent')
            if percent > 50:
                log_data = {
                    'type': 'danger',
                    'resource': 'ram',
                    'ip': self.server_info.get('ip'),
                    'percent': percent,
                    'time': datetime.now().strftime(DATETIME_FORMAT)
                }
                self.emit(manager='logger', tp='ram', payload=log_data, is_global=True)
            elif payload.get('percent') > 5:
                log_data = {
                    'type': 'warning',
                    'resource': 'ram',
                    'ip': self.server_info.get('ip'),
                    'percent': percent,
                    'time': datetime.now().strftime(DATETIME_FORMAT)
                }
                self.emit(manager='logger', tp='ram', payload=log_data, is_global=True)
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(3)
            if exit_event.is_set():
                break

    def collect_network(self, manager, tp):
        while True:
            payload = Resource().net()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(3)
            if exit_event.is_set():
                break

    def collect_cpu(self, manager, tp):
        while True:
            payload = Resource().cpu()
            percent: float = payload.get('avg')
            if percent > 90:
                log_data = {
                    'type': 'danger',
                    'resource': 'cpu',
                    'ip': self.server_info.get('ip'),
                    'percent': percent,
                    'time': datetime.now().strftime(DATETIME_FORMAT)
                }
                self.emit(manager='logger', tp='cpu', payload=log_data, is_global=True)
            elif payload.get('avg') > 5:
                log_data = {
                    'type': 'warning',
                    'resource': 'cpu',
                    'ip': self.server_info.get('ip'),
                    'percent': percent,
                    'time': datetime.now().strftime(DATETIME_FORMAT)
                }
                self.emit(manager='logger', tp='cpu', payload=log_data, is_global=True)

            self.emit(manager=manager, tp=tp, payload=payload)
            if exit_event.is_set():
                break

    def collect_disk(self, manager, tp):
        while True:
            payload = Resource().disk()
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(3)
            if exit_event.is_set():
                break
        print(":: Shutdown Resource thread ... OK")

    def save_cpu_info(self, server_id):
        """SAVE list CPU in db"""
        self._server_id = server_id
        cpu_resouce = Resource().cpu()
        if cpu_resouce:
            list_cpu = []
            for cpu in cpu_resouce.get('cpus'):
                list_cpu.append(cpu['cpu_name'])

            data_insert = ','.join(list_cpu)
            cpu_entity = CPU()
            cpu_entity.save(server_id, data_insert)

            # Commit in transaction save info server
            cpu_entity.db.commit()

    def collect_all(self, manager, tp):
        """
        Get all resources on machine 
        """
        while True:
            payload = dict(
                machine=dict(
                    ip_address=self.server_info.get('ip'),
                    hostname=self.server_info.get('hostname')
                ),
                resource=dict(
                    ram=Resource().ram(),
                    cpu=Resource().cpu(),
                    disk=Resource().disk(),
                )
            )
            self.emit(manager=manager, tp=tp, payload=payload)
            time.sleep(1)
            if exit_event.is_set():
                break

    def exec(self, server_id):
        """Split thread emit parallel resources collected"""
        # Save info database
        self.save_cpu_info(server_id)
        try:
            collect_all_resource_thread = \
                Thread(target=self.collect_all,
                       args=('resources', '*'))
            collect_all_resource_thread.start()

            collect_ram_thread = \
                Thread(target=self.collect_ram, args=(
                    'resources', 'ram'))
            collect_ram_thread.start()

            collect_cpu_thread = \
                Thread(target=self.collect_cpu, args=(
                    'resources', 'cpu'))
            collect_cpu_thread.start()

            collect_net_thread = \
                Thread(target=self.collect_network, args=(
                    'resources', 'net'))
            collect_net_thread.start()

            collect_disk_thread = \
                Thread(target=self.collect_disk, args=(
                    'resources', 'disk'))
            collect_disk_thread.start()

            collect_ram_thread.join()
            collect_cpu_thread.join()
            collect_net_thread.join()
            collect_disk_thread.join()

        except Exception as ex:
            log_data = {
                'type': 'warning',
                'resource': 'cpu',
                'msg': f"Machine: {self.server_info.get('ip')}: ERROR: {ex}"
            }
            self.emit(manager='logger', tp='error', payload=log_data, is_global=True)
            raise


class ProcessEmitter(CollectorEmitter):
    def __init__(self, server_info) -> None:
        super().__init__(server_info)

    def exec(self):
        while True:
            process = Process().get_services()
            self.emit(manager='process', tp='all', payload={
                'process': process
            })
            time.sleep(3)
            if exit_event.is_set():
                break
        print(':: Shutdown Process thread ... OK')
