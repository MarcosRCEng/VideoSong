from __future__ import annotations

from src.videosong.ui.wizard_state import WizardState


def is_valid_url(value: str) -> bool:
    url = value.strip()
    return url.startswith("http://") or url.startswith("https://")


def build_destination_label(destination: str) -> str:
    clean_destination = destination.strip()

    if not clean_destination:
        return "Passo 2: escolha uma pasta de destino para concluir a preparacao do fluxo."

    return f"Pasta de destino: {clean_destination}"


def build_urls_label(urls: list[str]) -> str:
    if not urls:
        return "Nenhuma URL adicionada ainda."

    return f"{len(urls)} URL(s) na lista atual."


def build_flow_summary(state: WizardState) -> str:
    destination = state.destination.strip()

    if not state.destination.strip():
        return "Passo 2: formato selecionado. Escolha a pasta de destino para concluir a preparacao."

    if not state.urls:
        return f"Passo 3: pasta definida em {destination}. Adicione ao menos uma URL valida para liberar a revisao final."

    mode_label = "video" if state.mode == "video" else "audio"
    first_url = state.primary_url
    return (
        f"Passo 4: formato {mode_label} selecionado, pasta definida em {destination} e {len(state.urls)} URL(s) pronta(s). "
        f"Nesta sprint, o download sera iniciado pela primeira URL da lista: {first_url}."
    )
