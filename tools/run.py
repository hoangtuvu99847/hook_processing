import json
import os
import sys
from src.main import main as run_collection_tool
from src.collector.emitter import CollectorEmitter
import socket

print("+==========================================+")
print("+           Copyright (c) 2021             +")
print("+          -- Nguyễn Viết Vũ --            +")
print("+        Project: Hook Processing          +")
print("+==========================================+")


# Get IP address of machine
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP = None
try:
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
except Exception:
    IP = '127.0.0.1'
finally:
    s.close()

if __name__ == '__main__':
    machine = {
        'hostname': socket.gethostname(),
        'ip': IP
    }
    try:
        run_collection_tool(machine)
    except KeyboardInterrupt:
        CollectorEmitter(machine).disconnect()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
