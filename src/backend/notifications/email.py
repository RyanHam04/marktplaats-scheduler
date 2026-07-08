from .base import Notifier


class EmailNotifier(Notifier):
    def __init__(self):
        raise NotImplementedError

    def send(self, message: str) -> None:
        raise NotImplementedError
