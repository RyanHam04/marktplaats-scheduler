from backend.notifications.base import Notifier
from backend.notifications.email import EmailNotifier
from backend.notifications.ntfy import NtfyNotifier
from backend.notifications.telegram import TelegramNotifier
from backend.api.schemas.notifiers import (
    NotifierParams,
    NtfyNotifierParams,
    TelegramNotifierParams,
    EmailNotifierParams,
)


def create_notifier(params: NotifierParams) -> Notifier:
    match params:
        case NtfyNotifierParams():
            return NtfyNotifier(params)
        case TelegramNotifierParams():
            return TelegramNotifier(params)
        case EmailNotifierParams():
            return EmailNotifier(params)


def compose_message(listings):
    pass
