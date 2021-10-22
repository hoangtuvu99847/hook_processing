import time
import os
import sys
from src.main import main as run_collection_tool
from src.collector.emitter import CollectorEmitter
from src.sk import HOSTNAME, IP

print("+==========================================+")
print("+           Copyright (c) 2021             +")
print("+          -- Nguyễn Viết Vũ --            +")
print("+        Project: Hook Processing          +")
print("+==========================================+")


def clean_up_thread():
    print('Clean up!')
    print('Done!')


if __name__ == '__main__':
    machine = {
        'hostname': HOSTNAME,
        'ip': IP
    }
    try:
        run_collection_tool(machine)
    except KeyboardInterrupt:
        clean_up_thread()
        CollectorEmitter(machine).disconnect()
        try:
            sys.exit()
        except SystemExit:
            os._exit(0)
