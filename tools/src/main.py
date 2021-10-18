# -*- coding: utf-8 -*-
from src.collector.emitter import ResourcesEmitter
from src.consumer.observe import Observe
from src.db.models import Server
import paho.mqtt.subscribe as subscribe
from threading import Thread
import socket


def main(machine):
    resource_prod = ResourcesEmitter(server_info=machine)
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
        publisher = Thread(target=resource_prod.exec,
                           args=(server_id, ))
        # Collection process action
        ...
        # Consumer action
        consumer = Thread(target=consumer_prod.callback,
                          args=(machine.get('ip'), ))

        consumer.start()
        publisher.start()

        consumer.join()
        publisher.join()
