from __future__ import annotations

from src.videosong.ui.wizard_state import WizardState


def is_valid_url(value: str) -> bool:
    url = value.strip()
    return url.startswith("http://") or url.startswith("https://")


def build_destination_label(destination: str) -> str:
    clean_destination = destination.strip()

    if not clean_destination:
        return "Passo 3: escolha uma pasta de destino para concluir a preparacao do fluxo."

    return f"Pasta de destino: {clean_destination}"


def build_flow_summary(state: WizardState) -> str:
    if not state.url.strip():
        return "Passo 1: cole a URL do video para liberar a validacao do fluxo."

    if not is_valid_url(state.url):
        return "Passo 1: use uma URL completa com http:// ou https:// para continuar."

    if not state.destination.strip():
        return "Passo 3: formato selecionado. Escolha a pasta de destino para concluir a preparacao."

    mode_label = "video" if state.mode == "video" else "audio"
    return (
        f"Passo 3: formato {mode_label} selecionado e pasta definida. "
        f"O fluxo esta pronto para iniciar o download em {state.destination.strip()}."
    )


def build_status_feedback(state: WizardState) -> tuple[str, str]:
    if not state.url.strip():
        return ("error", "Erro: informe uma URL antes de continuar.")

    if not is_valid_url(state.url):
        return ("error", "Erro: use uma URL valida com http:// ou https://.")

    if not state.destination.strip():
        return ("error", "Erro: escolha uma pasta de destino antes de continuar.")

    mode_label = "video" if state.mode == "video" else "audio"
    return (
        "success",
        (
            f"Fluxo validado: URL pronta, formato {mode_label} selecionado e destino definido em {state.destination.strip()}. "
            "Tudo pronto para iniciar o download."
        ),
    )
