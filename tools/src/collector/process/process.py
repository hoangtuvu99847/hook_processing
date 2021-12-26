# from src import PROCESS_PROPS
import psutil
from time import sleep
from src.config import PROCESS_PROPERTIES_CONFIG_SHOWN


class Process:
    """Observe process runing and handle action with process"""

    def get_services(self):
        procs = []
        for proc in psutil.process_iter():
            pinfo = proc.as_dict(PROCESS_PROPERTIES_CONFIG_SHOWN)
            pinfo.update({'pid': proc.pid})
            pinfo['memory_percent'] = round(
                pinfo['memory_percent'], 1) if pinfo['memory_percent'] else None
            procs.append(pinfo)
        procs = sorted(procs, key=lambda proc: proc.get('cpu_percent')
                       if proc.get('cpu_percent') else 0, reverse=True)
        return procs

    def show(self):
        services: list = self.get_services()
        print(services)
        return services


if __name__ == "__main__":
    Process().show()
