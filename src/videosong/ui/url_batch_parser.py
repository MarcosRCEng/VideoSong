from __future__ import annotations

from dataclasses import dataclass

from src.videosong.ui.wizard_messages import is_valid_url

EMPTY_BATCH_ERROR = "Erro: cole ao menos uma URL para adicionar em lote."


@dataclass(slots=True)
class ParsedUrlBatch:
    accepted_urls: list[str]
    invalid_entries: list[str]
    duplicate_urls: list[str]

    @property
    def has_changes(self) -> bool:
        return bool(self.accepted_urls)


def parse_url_batch(value: str, existing_urls: list[str] | None = None) -> ParsedUrlBatch:
    existing = set(existing_urls or [])
    accepted_urls: list[str] = []
    invalid_entries: list[str] = []
    duplicate_urls: list[str] = []

    for raw_line in value.splitlines():
        candidate = raw_line.strip()
        if not candidate:
            continue

        if not is_valid_url(candidate):
            invalid_entries.append(candidate)
            continue

        if candidate in existing:
            duplicate_urls.append(candidate)
            continue

        existing.add(candidate)
        accepted_urls.append(candidate)

    return ParsedUrlBatch(
        accepted_urls=accepted_urls,
        invalid_entries=invalid_entries,
        duplicate_urls=duplicate_urls,
    )


def validate_url_batch(value: str) -> str | None:
    if not any(line.strip() for line in value.splitlines()):
        return EMPTY_BATCH_ERROR

    return None


def build_batch_feedback(result: ParsedUrlBatch) -> tuple[str, str]:
    if not result.has_changes and result.invalid_entries:
        return (
            "error",
            f"Erro: nenhuma URL valida foi adicionada. Entradas invalidas: {_format_entries(result.invalid_entries)}.",
        )

    if not result.has_changes and result.duplicate_urls:
        return (
            "error",
            f"Erro: as URL(s) coladas ja estavam na lista: {_format_entries(result.duplicate_urls)}.",
        )

    details: list[str] = [f"{len(result.accepted_urls)} URL(s) adicionada(s) em lote."]
    if result.invalid_entries:
        details.append(f"Ignoradas por serem invalidas: {_format_entries(result.invalid_entries)}.")
    if result.duplicate_urls:
        details.append(f"Ignoradas por duplicidade: {_format_entries(result.duplicate_urls)}.")

    return ("neutral", " ".join(details))


def _format_entries(values: list[str]) -> str:
    preview = ", ".join(values[:3])
    if len(values) <= 3:
        return preview

    return f"{preview} e mais {len(values) - 3}"
