from dataclasses import dataclass


@dataclass(frozen=True)
class DownloadPlan:
    url: str
    mode: str
    destination: str

    @property
    def mode_label(self) -> str:
        if self.mode == "audio":
            return "Audio"

        return "Video"

    @property
    def mode_description(self) -> str:
        if self.mode == "audio":
            return "Extrair somente o audio do link informado."

        return "Baixar o video completo do link informado."

    @property
    def has_url(self) -> bool:
        return bool(self.url)

    @property
    def has_destination(self) -> bool:
        return bool(self.destination)

    @property
    def is_ready(self) -> bool:
        return self.has_url and self.has_destination


def build_download_plan(url: str, mode: str, destination: str) -> DownloadPlan:
    clean_mode = "audio" if mode == "audio" else "video"

    return DownloadPlan(
        url=url.strip(),
        mode=clean_mode,
        destination=destination.strip(),
    )


def build_destination_label(plan: DownloadPlan) -> str:
    if not plan.has_destination:
        return "Nenhuma pasta selecionada ainda."

    return f"Pasta de destino: {plan.destination}"


def build_flow_summary(plan: DownloadPlan) -> str:
    destination_label = build_destination_label(plan)

    if not plan.has_url:
        return "Cole uma URL para liberar a revisao do download."

    if not plan.has_destination:
        return (
            f"URL pronta para baixar em modo {plan.mode_label.lower()}: {plan.url}. "
            f"{plan.mode_description} Escolha a pasta de destino para concluir a preparacao."
        )

    return (
        f"Pronto para baixar em modo {plan.mode_label.lower()}: {plan.url}. "
        f"{plan.mode_description} {destination_label}"
    )


def build_download_checklist(plan: DownloadPlan) -> str:
    url_status = "ok" if plan.has_url else "pendente"
    destination_status = "ok" if plan.has_destination else "pendente"
    readiness = "Pronto para integrar o download." if plan.is_ready else "Falta concluir os campos pendentes."

    return (
        f"URL: {url_status}\n"
        f"Formato: {plan.mode_label}\n"
        f"Pasta: {destination_status}\n"
        f"{readiness}"
    )
