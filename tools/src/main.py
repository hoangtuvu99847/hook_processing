# -*- coding: utf-8 -*-
from src.collector.emitter import ProcessEmitter, ResourcesEmitter
from src.consumer.observe import Observe
from src.db.models import Server
from threading import Thread
import concurrent.futures

from src.thread.collection import CollectionThread


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

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     concurrencies = []
        #     concurrencies.append(
        #         executor.submit(resource_prod.exec, server_id),
        #         executor.submit(process_prod.exec),
        #         executor.submit(consumer_prod.callback, machine.get('ip')),
        #     )
        #     for f in concurrent.futures.as_completed(concurrencies):
        #         pass

        resource_publisher = CollectionThread(target=resource_prod.exec,
                                              args=(server_id, ))
        resource_publisher.start()

        # Collection process action
        process_publisher = CollectionThread(target=process_prod.exec)
        process_publisher.start()

        # Consumer action
        # consumer = CollectionThread(target=consumer_prod.callback,
        #                             args=(machine.get('ip'), ))
        # consumer.start()

        # consumer.join()
        resource_publisher.join()
        process_publisher.join()
