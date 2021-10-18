# from src import PROCESS_PROPS
import psutil
from time import sleep


class Process:
    """Observe process runing and handle action with process"""

    def __init__(self):
        self.__process_map = ['name', 'username']

    def get_services(self):
        procs: list = [
            dict(pid=proc.pid,
                 info=proc.info)
            for proc in psutil.process_iter(self.__process_map)
        ]
        return procs

    def kill(self):
        pass

    def show(self):
        while True:
            services: list = self.get_services()
            print(services)
            """
            Emit action 
            """
            sleep(1)


if __name__ == "__main__":
    Process().show()
