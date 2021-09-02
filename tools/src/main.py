# -*- coding: utf-8 -*-
from src.producer import Producer
from src.db import Server
from src import hostname, ip
import asyncio
print("+==========================================+")
print("+           Copyright (c) 2021             +")
print("+          -- Nguyễn Viết Vũ --            +")
print("+        Project: Hook Processing          +")
print("+==========================================+")


producer = Producer(server_info={
    'hostname': hostname,
    'ip': ip
})


def execute():
    server = Server()
    result_save = server.save(hostname=hostname, ip_address=ip)
    if result_save:
        print("Start sending data packet ...")
        print("====================================")
        print('If you want to quit. Press Ctrl + C.')
        asyncio.run(producer.produce())
