import psutil
import sys


class CollectionTool:
    def __init__(self):
        self.THRESHOLD = 100 * 1024 * 1024  # 100MB

    @staticmethod
    def bytes2human(n):
        # http://code.activestate.com/recipes/578019
        # >>> bytes2human(10000)
        # '9.8K'
        # >>> bytes2human(100001221)
        # '95.4M'
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

    def ram(self):
        memory = psutil.virtual_memory()
        total = self.bytes2human(psutil.virtual_memory().total)
        ram_obj = {
            'total': total,
            'percent': memory.percent
        }
        return ram_obj

    def cpu_per(self):
        cpu_per = psutil.cpu_percent(interval=1, percpu=True)
        list_cpu = []
        for i, core_per in enumerate(cpu_per):
            cpu_dict = {}
            cpu_dict['cpu_name'] = 'cpu_{count}'.format(count=i+1)
            cpu_dict['percent'] = core_per
            list_cpu.append(cpu_dict)
        return list_cpu

    def cpu_avg(self):
        percent = psutil.cpu_percent()
        return percent

    def disk(self):
        disk = psutil.disk_usage('/')
        total = self.bytes2human(disk.total)
        used = self.bytes2human(disk.used)
        free = self.bytes2human(disk.free)
        percent = disk.percent
        return {
            'total': total,
            'used': used,
            'free': free,
            'percent': percent
        }

    def network(self):
        net = psutil.net_io_counters()
        sent = self.bytes2human(net.bytes_sent)
        recv = self.bytes2human(net.bytes_recv)
        error_in = net.errin
        error_out = net.errout
        return {
            'sent': sent,
            'recv': recv,
            'error_in': error_in,
            'error_out': error_out,
        }

    def sensor(self):
        list_cpu_temp = []
        if not hasattr(psutil, "sensors_temperatures"):
            sys.exit("platform not supported")
        temps = psutil.sensors_temperatures()
        if not temps:
            sys.exit("can't read any temperature")
        if 'coretemp' in temps:
            for entries in temps['coretemp']:
                temp = {
                    'label': entries.label,
                    'current': entries.current,
                    'high': entries.high,
                    'critical': entries.critical,
                }
                list_cpu_temp.append(temp)
        return list_cpu_temp

    def _ex(self):
        pass

    def run(self):
        try:

            cpu_list = self.cpu_per()
            ram_status = self.ram()
            sensor_status = self.sensor()
            disk_status = self.disk()
            network_status = self.network()
            cpu_avg = self.cpu_avg()
            data = {
                'cpu': {
                    'cpu_avg': cpu_avg,
                    'list_cpu': cpu_list,
                    'core': psutil.cpu_count(logical=False),
                    'thread': psutil.cpu_count()
                },
                'ram': ram_status,
                'sensor': sensor_status,
                'disk': disk_status,
                'network': network_status
            }
            return data

        except Exception as ex:
            print(ex)
            pass
