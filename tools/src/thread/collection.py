
import threading
import signal

exit_event = threading.Event()


def signal_handle(signum, frame):
    print('SIGNAL')
    exit_event.set()


signal.signal(signal.SIGINT, signal_handle)


class CollectionThread(threading.Thread):
    def __init__(self, *args, **kwargs) -> None:
        super(CollectionThread, self).__init__(*args, **kwargs)
        self._stopevent = threading.Event()
        self._sleepperior = 1.0

    def run(self) -> None:
        return super().run()

    def join(self, timeout=None) -> None:
        """Stop the thread."""
        self._stopevent.set()
        return super().join(timeout=self._sleepperior)


if __name__ == "__main__":
    CollectionThread()
