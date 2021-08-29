import os
import sys
from src.main import execute as run_tool
from src.main import producer

if __name__ == '__main__':
    try:
        run_tool()
    except KeyboardInterrupt:
        print('Interrupted')
        producer.disconnect()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)