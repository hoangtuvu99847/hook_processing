import psutil
import sys


class CollectionTool:
    def __init__(self):
        self.THRESHOLD = 100 * 1024 * 1024  # 100MB

    @staticmethod
    def convert_byte_to_gb(value):
        return round(value / (1024.0 ** 3), 1)

    def ram(self):
        memory = psutil.virtual_memory()

        ram_obj = {
            'available': memory.available,
            'total': self.convert_byte_to_gb(psutil.virtual_memory().total),
            'percent': memory.percent
        }
        return ram_obj

    def cpu(self):
        cpu_per = psutil.cpu_percent(interval=1, percpu=True)
        cpu_dict = {}
        for i, core_per in enumerate(cpu_per):
            cpu_dict['cpu_{count}'.format(count=i+1)] = core_per
        return cpu_dict

    def disk(self):
        pass

    def network(self):
        pass

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

            cpu_status = self.cpu()
            ram_status = self.ram()
            sensor_status = self.sensor()
            disk_status = self.disk()
            network_status = self.network()
            data = {
                'cpu': cpu_status,
                'ram': ram_status,
                'sensor': sensor_status,
                'disk': disk_status,
                'network': network_status
            }
            return data

        except Exception as ex:
            print(ex)
            pass
