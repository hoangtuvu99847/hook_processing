# -*- coding: utf-8 -*-
from src.producer import Producer
from src.db import Server
import asyncio
import socket
print("+==========================================+")
print("+           Copyright (c) 2021             +")
print("+          -- Nguyễn Viết Vũ --            +")
print("+        Project: Hook Processing          +")
print("+==========================================+")


def get_ip_machine():
    """
    This function to get local ip for current machine
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


hostname = socket.gethostname()
ip = get_ip_machine()

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
