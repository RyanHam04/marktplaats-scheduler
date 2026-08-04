from .base import Notifier
from ..api.schemas.notifiers import EmailNotifierParams


class EmailNotifier(Notifier):
    def __init__(self,  params: EmailNotifierParams):
        raise NotImplementedError

    def send(self, message: str) -> None:
        raise NotImplementedError
