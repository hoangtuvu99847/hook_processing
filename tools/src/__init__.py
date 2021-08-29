__version__ = "1.0.0"
__author__: str = "vunv"
__license__: str
__copyright__: str


WAIT_TIME = 1
THRESHOLD = 100 * 1024 * 1024
DISK_USAGE_PATH = '/'
PROCESS_PROPS = ['name', 'username']
MAIN_TOPIC = 'server/'

try:
    from yaml import load, CLoader as Loader
except ImportError:
    from yaml import Loader

with open("config.yml", "r") as ymlfile:
    cfg = load(ymlfile, Loader=Loader)
