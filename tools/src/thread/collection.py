
import threading


class CollectionThread(threading.Thread):
    def __init__(self, target, args, kwargs) -> None:
        super().__init__(target=target, args=args, kwargs=kwargs, daemon=False)


if __name__ == "__main__":
    CollectionThread()
