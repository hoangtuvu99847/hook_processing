from collection import PROCESS_PROPS
from typing import List
import psutil
from time import sleep


class Process:
    def __init__(self):
        self.__process_map: list = PROCESS_PROPS

    def get_services(self) -> List[dict]:
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
