
from yaml import load
import socket
from src.db import Server
from src.producer import Producer

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open("config.yml", "r") as ymlfile:
    cfg = load(ymlfile, Loader=Loader)


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
        producer.produce()
