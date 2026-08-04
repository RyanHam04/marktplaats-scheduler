from .base import Notifier
from ..api.schemas.notifiers import TelegramNotifierParams


class TelegramNotifier(Notifier):
    def __init__(self, params: TelegramNotifierParams):
        raise NotImplementedError

    def send(self, message: str) -> None:
        raise NotImplementedError
