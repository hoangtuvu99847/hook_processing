# -*- coding: utf-8 -*-
from src.collector.emitter import ProcessEmitter, ResourcesEmitter
from src.consumer.observe import Observe
from src.db.models import Server
from threading import Thread


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
                                    args=(server_id, ), daemon=True)
        resource_publisher.start()

        # Collection process action
        process_publisher = Thread(target=process_prod.exec, daemon=True)
        process_publisher.start()

        # Consumer action
        consumer = Thread(target=consumer_prod.callback,
                          args=(machine.get('ip'), ), daemon=True)
        consumer.start()

        consumer.join()
        resource_publisher.join()
        process_publisher.join()
