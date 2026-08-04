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
    if isinstance(params, NtfyNotifierParams):
        return NtfyNotifier(params)

    if isinstance(params, TelegramNotifierParams):
        return TelegramNotifier(params)

    if isinstance(params, EmailNotifierParams):
        return EmailNotifier(params)

def compose_message(listings) -> str:
    lines = [f"{len(listings)} Marktplaats listings found", ""]

    for listing in listings[:10]:
        lines.append(
            f"{listing.title}\n"
            f"{listing.price_as_string(lang='nl')}\n"
            f"{listing.link}\n"
        )

    return "\n".join(lines)