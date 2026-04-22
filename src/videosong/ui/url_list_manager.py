from __future__ import annotations

from typing import Final

from src.videosong.ui.wizard_messages import is_valid_url

EMPTY_URL_ERROR: Final[str] = "Erro: informe uma URL antes de adicionar."
INVALID_URL_ERROR: Final[str] = "Erro: use uma URL valida com http:// ou https://."


def validate_url_to_add(value: str) -> str | None:
    candidate = value.strip()

    if not candidate:
        return EMPTY_URL_ERROR

    if not is_valid_url(candidate):
        return INVALID_URL_ERROR

    return None


def add_url(urls: list[str], value: str) -> tuple[list[str], str | None]:
    error = validate_url_to_add(value)

    if error:
        return urls.copy(), error

    candidate = value.strip()
    return [*urls, candidate], None


def remove_url(urls: list[str], index: int) -> list[str]:
    if index < 0 or index >= len(urls):
        return urls.copy()

    return [url for position, url in enumerate(urls) if position != index]
