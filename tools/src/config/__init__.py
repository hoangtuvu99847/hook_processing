WAIT_TIME = 1
THRESHOLD = 100 * 1024 * 1024
DISK_USAGE_PATH = '/'
PROCESS_PROPS = ['name', 'username']
MAIN_TOPIC = 'server/'


class MySQLConf:
    HOST = '35.240.161.144'
    USER = 'vunv'
    PASSWORD = 'Vu@1479825'
    DB = 'hook_processing'


class MQTTConf:
    HOST = '35.240.161.144'

    class PORT:
        TCP = 1883
        WEBSOCKET = 8000
        BROKER = 8080
