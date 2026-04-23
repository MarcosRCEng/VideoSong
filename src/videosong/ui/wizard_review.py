from __future__ import annotations

from src.videosong.services.download_queue import DownloadItem
from src.videosong.ui.wizard_state import WizardState


def build_review_summary(state: WizardState, download_items: list[DownloadItem] | None = None) -> str:
    queue = download_items or state.download_items
    destination = state.destination.strip() or "Nao selecionada"
    readiness = build_review_readiness_label(state)
    queue_totals = build_download_queue_totals(queue)
    queue_lines = build_download_items_summary(queue)

    return "\n".join(
        [
            f"Formato: {_build_mode_label(state.mode)}",
            f"Pasta de destino: {destination}",
            f"Quantidade de URLs: {len(state.urls)}",
            f"Estado: {readiness}",
            "Execucao desta sprint: todas as URLs da fila serao processadas em ordem, uma por vez.",
            (
                "Resumo global da fila: "
                f"Total {queue_totals['total']} | "
                f"Concluidos {queue_totals['completed']} | "
                f"Erros {queue_totals['error']} | "
                f"Em andamento {queue_totals['running']}"
            ),
            "Fila atual:",
            *queue_lines,
        ]
    )


def build_review_readiness_label(state: WizardState) -> str:
    missing_fields = _collect_missing_fields(state)

    if not missing_fields:
        return "pronto para execucao."

    if len(missing_fields) == 1:
        return f"pendente, falta {missing_fields[0]}."

    return f"pendente, faltam {', '.join(missing_fields[:-1])} e {missing_fields[-1]}."


def can_advance_from_step(state: WizardState) -> bool:
    return get_next_step_blocker(state) is None


def get_next_step_blocker(state: WizardState) -> str | None:
    active_key = state.active_step.key

    if active_key == "destination" and not state.destination.strip():
        return "Escolha uma pasta de destino antes de avancar."

    if active_key == "urls" and not state.urls:
        return "Adicione ao menos uma URL valida antes de avancar."

    return None


def build_status_feedback(state: WizardState) -> tuple[str, str]:
    if not state.destination.strip():
        return ("error", "Erro: escolha uma pasta de destino antes de continuar.")

    if not state.urls:
        return ("error", "Erro: adicione ao menos uma URL valida antes de continuar.")

    mode_label = "video" if state.mode == "video" else "audio"
    return (
        "success",
        (
            f"Revisao concluida: {len(state.urls)} URL(s), formato {mode_label} e destino definido em {state.destination.strip()}. "
            "Nesta sprint, a fila sera executada em ordem e continuara para os proximos itens mesmo se algum download falhar."
        ),
    )


def _build_mode_label(mode: str) -> str:
    if mode == "audio":
        return "Somente audio"

    return "Video completo"


def build_download_items_summary(download_items: list[DownloadItem]) -> list[str]:
    if not download_items:
        return ["Nenhum item na fila ainda."]

    return [
        f"{index}. {build_short_url(item.url)} | {build_status_label(item.status)} | {item.message}"
        for index, item in enumerate(download_items, start=1)
    ]


def build_short_url(url: str, max_length: int = 48) -> str:
    clean_url = url.strip()

    if len(clean_url) <= max_length:
        return clean_url

    return f"{clean_url[: max_length - 3].rstrip('/')}..."


def build_status_label(status: str) -> str:
    labels = {
        "pending": "Aguardando",
        "running": "Baixando",
        "completed": "Concluido",
        "error": "Erro",
    }
    return labels.get(status, "Desconhecido")


def build_download_queue_totals(download_items: list[DownloadItem]) -> dict[str, int]:
    return {
        "total": len(download_items),
        "completed": sum(1 for item in download_items if item.status == "completed"),
        "error": sum(1 for item in download_items if item.status == "error"),
        "running": sum(1 for item in download_items if item.status == "running"),
    }


def _collect_missing_fields(state: WizardState) -> list[str]:
    missing_fields: list[str] = []

    if not state.destination.strip():
        missing_fields.append("a pasta de destino")

    if not state.urls:
        missing_fields.append("a lista de URLs")

    return missing_fields
