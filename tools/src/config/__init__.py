WAIT_TIME = 1
THRESHOLD = 100 * 1024 * 1024
DISK_USAGE_PATH = '/'
PROCESS_PROPS = ['name', 'username']
MAIN_TOPIC = 'server/'

PROCESS_PROPERTIES_CONFIG_SHOWN = ['name', 'username',
                                   'memory_percent', 'cpu_percent', 'status']


class MySQLConf:
    HOST = '10.130.64.113'
    USER = 'vunv79'
    PASSWORD = 'Vu@1479825'
    DB = 'hook_processing'


class MQTTConf:
    HOST = '10.130.64.113'

    class PORT:
        TCP = 1883
        WEBSOCKET = 8000
        BROKER = 8080
