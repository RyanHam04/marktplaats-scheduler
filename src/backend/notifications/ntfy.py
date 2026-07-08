import token

from .base import Notifier
from python_ntfy import NtfyClient

from ..api.schemas.notifiers import NtfyNotifierParams


class NtfyNotifier(Notifier):
    def __init__(self, params: NtfyNotifierParams):
        # Params it should accept:
        # Topic + ((Username + Password) xor Token)
        auth = (
            (params.username, params.password)
            if params.username and params.password
            else None
        )
        if params.token:
            auth = params.token
        elif params.username and params.password:
            auth = (params.username, params.password)
        else:
            auth = None

        self.client = NtfyClient(
            topic=params.topic,
            auth=auth,
        )

    def send(self, message: str) -> None:
        self.client.send(message)
