from os import O_ASYNC
import os
import platform
from time import time, sleep
from src import DISK_USAGE_PATH, THRESHOLD, WAIT_TIME
from psutil._common import bytes2human
from typing import Any, Dict, List, Tuple
import psutil
import sys


class Resource:
    """
    This is a class that describes properties for collecting
    """

    def __init__(self) -> None:
        self.THRESHOLD: int = THRESHOLD  # 100MB
        self.wait: int = WAIT_TIME
        self.disk_usage: str = DISK_USAGE_PATH

    @staticmethod
    def ram() -> Dict[str, float]:
        try:
            memory = psutil.virtual_memory()
            total: str = bytes2human(psutil.virtual_memory().total)
            return dict(total=total, percent=memory.percent)
        except Exception as ex:
            print('[ERROR] :: Collection :: Resource :: mem() -> ', ex)

    def cpu(self) -> Dict[str, Any]:
        try:
            cpu_per = psutil.cpu_percent(percpu=True)
            list_cpu: list = []
            cpu_percent: Dict[str, Any]
            for i, core_per in enumerate(cpu_per):
                cpu_dict: Dict[str, Any] = {}
                cpu_dict['cpu_name'] = 'cpu_{count}'.format(count=i+1)
                cpu_dict['percent'] = core_per
                list_cpu.append(cpu_dict)
            cpu_percent: Dict = psutil.cpu_percent()
            return dict(
                avg=cpu_percent,
                cpus=list_cpu
            )
        except Exception as ex:
            print('[ERROR] :: Collection :: Resource :: cpu() -> ', ex)

    def disk(self) -> Dict[str, Any]:
        try:
            disk = psutil.disk_usage(self.disk_usage)
            total: int = disk.total
            used: str = bytes2human(disk.used)
            free: str = bytes2human(disk.free)
            percent: float = disk.percent
            return dict(
                total=total,
                used=used,
                free=free,
                percent=percent
            )

        except Exception as ex:
            print('[ERROR] :: Collection :: Resource :: disk() -> ', ex)

    def sensor(self):
        sys = platform.system()
        if sys == 'Windows' or sys == 'Darwin':
            return
        try:
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
        except Exception as ex:
            print('[ERROR] :: Collection :: Resource :: sensor() -> ', ex)

    @staticmethod
    def net():
        try:
            network = psutil.net_io_counters()
            sent: str = bytes2human(network.bytes_sent)
            recv: str = bytes2human(network.bytes_recv)
            error_in: int = network.errin
            error_out: int = network.errout
            return dict(
                sent=sent,
                recv=recv,
                error_in=error_in,
                error_out=error_out,
            )
        except Exception as ex:
            print('[ERROR] :: Collection :: Resource :: net() -> ', ex)

    def collect(self):
        while True:
            r = self.net()
            print(r)
