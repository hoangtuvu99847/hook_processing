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


if __name__ == '__main__':
    machine = {
        'hostname': HOSTNAME,
        'ip': IP
    }
    try:
        run_collection_tool(machine)
    except KeyboardInterrupt:
        CollectorEmitter(machine).disconnect()
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(0)
