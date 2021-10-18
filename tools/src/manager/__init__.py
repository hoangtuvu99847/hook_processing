__version__ = "1.0.0"
import socket


__author__: str = "vunv"
__license__: str
__copyright__: str


WAIT_TIME = 1
THRESHOLD = 100 * 1024 * 1024
DISK_USAGE_PATH = '/'
PROCESS_PROPS = ['name', 'username']
MAIN_TOPIC = 'server/'

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

from config import *