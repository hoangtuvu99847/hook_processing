import time
import os
import sys
from src.main import main as run_collection_tool
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
        try:
            sys.exit()
        except SystemExit:
            os._exit(0)
