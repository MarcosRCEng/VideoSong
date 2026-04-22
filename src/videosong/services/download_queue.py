from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

DownloadItemStatus = Literal["pending", "running", "completed", "error"]
DOWNLOAD_ITEM_STATUSES: tuple[DownloadItemStatus, ...] = ("pending", "running", "completed", "error")

DEFAULT_STATUS_MESSAGES: dict[DownloadItemStatus, str] = {
    "pending": "Aguardando processamento.",
    "running": "Preparando download.",
    "completed": "Download concluido com sucesso.",
    "error": "Falha ao processar o download.",
}


@dataclass(slots=True, frozen=True)
class DownloadItem:
    url: str
    mode: str
    destination: str
    status: DownloadItemStatus = "pending"
    message: str = DEFAULT_STATUS_MESSAGES["pending"]


def build_download_item(url: str, mode: str, destination: str) -> DownloadItem:
    clean_url = url.strip()
    clean_mode = "audio" if mode == "audio" else "video"
    clean_destination = destination.strip()
    return DownloadItem(
        url=clean_url,
        mode=clean_mode,
        destination=clean_destination,
    )


def build_download_queue(urls: list[str], mode: str, destination: str) -> list[DownloadItem]:
    return [build_download_item(url, mode, destination) for url in urls]


def update_download_item(
    item: DownloadItem,
    *,
    status: DownloadItemStatus,
    message: str | None = None,
) -> DownloadItem:
    validate_download_item_status(status)
    next_message = (message or DEFAULT_STATUS_MESSAGES[status]).strip()
    return replace(item, status=status, message=next_message)


def validate_download_item_status(status: str) -> None:
    if status not in DOWNLOAD_ITEM_STATUSES:
        raise ValueError(f"Estado de download invalido: {status}")
