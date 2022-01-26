# -*- coding: utf-8 -*-
from src.collector.emitter import ProcessEmitter, ResourcesEmitter
from src.consumer.observe import Observe
from src.db.models import Server
from threading import Thread
from src.signal.event import exit_event
from src.producer.mqtt import MQTT


def main(machine):
    resource_prod = ResourcesEmitter(server_info=machine)
    process_prod = ProcessEmitter(server_info=machine)
    consumer_prod = Observe()

    # Create instance machine is server

    server = Server()
    server_id = server.save(hostname=machine.get(
        'hostname'), ip_address=machine.get('ip'))
    if server_id:
        print("Start sending data packet ...")
        print("====================================")
        print('If you want to quit. Press Ctrl + C.')

        # Create thread execute action
        # Collection resource action

        resource_publisher = Thread(target=resource_prod.exec,
                                    args=(server_id,))
        resource_publisher.start()

        # Collection process action
        process_publisher = Thread(target=process_prod.exec)
        process_publisher.start()

        # Consumer action
        consumer = Thread(target=consumer_prod.callback,
                          args=(machine.get('ip'),))
        consumer.daemon = True
        consumer.start()

        resource_publisher.join()
        process_publisher.join()
        consumer.join
        if exit_event:
            mqtt = MQTT()
            client = mqtt.get_client
            client.disconnect()
            print('Terminated!')
