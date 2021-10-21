# Get IP address of machine
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP = None
try:
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
except Exception:
    IP = '127.0.0.1'
finally:
    s.close()
HOSTNAME = socket.gethostname()
