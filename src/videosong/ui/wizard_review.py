from __future__ import annotations

from src.videosong.ui.wizard_state import WizardState


def build_review_summary(state: WizardState) -> str:
    destination = state.destination.strip() or "Nao selecionada"
    readiness = build_review_readiness_label(state)

    return "\n".join(
        [
            f"Formato: {_build_mode_label(state.mode)}",
            f"Pasta de destino: {destination}",
            f"Quantidade de URLs: {len(state.urls)}",
            f"Estado: {readiness}",
            "Execucao desta sprint: todas as URLs da fila serao processadas em ordem, uma por vez.",
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


def _collect_missing_fields(state: WizardState) -> list[str]:
    missing_fields: list[str] = []

    if not state.destination.strip():
        missing_fields.append("a pasta de destino")

    if not state.urls:
        missing_fields.append("a lista de URLs")

    return missing_fields
