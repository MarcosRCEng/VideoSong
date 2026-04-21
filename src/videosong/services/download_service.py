from dataclasses import dataclass
from pathlib import Path

from yt_dlp import DownloadError, YoutubeDL


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
    def mode_next_step(self) -> str:
        if self.mode == "audio":
            return "Quando o download real for integrado, o arquivo final sera salvo como audio."

        return "Quando o download real for integrado, o arquivo final sera salvo como video."

    @property
    def has_url(self) -> bool:
        return bool(self.url)

    @property
    def has_destination(self) -> bool:
        return bool(self.destination)

    @property
    def is_ready(self) -> bool:
        return self.has_url and self.has_destination


@dataclass(frozen=True)
class StatusFeedback:
    tone: str
    message: str


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


def build_url_guidance(plan: DownloadPlan) -> str:
    if not plan.has_url:
        return "Cole a URL principal do video para liberar a proxima etapa."

    return f"URL pronta para uso: {plan.url}"


def build_mode_guidance(plan: DownloadPlan) -> str:
    return f"{plan.mode_description} {plan.mode_next_step}"


def build_review_button_label(plan: DownloadPlan) -> str:
    if plan.mode == "audio":
        return "Baixar audio"

    return "Baixar video"


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
    readiness = "Pronto para iniciar o download." if plan.is_ready else "Falta concluir os campos pendentes."

    return (
        f"URL: {url_status}\n"
        f"Formato: {plan.mode_label}\n"
        f"Pasta: {destination_status}\n"
        f"{readiness}"
    )


def build_review_status(plan: DownloadPlan) -> StatusFeedback:
    if not plan.has_url:
        return StatusFeedback(
            tone="error",
            message="Informe uma URL para continuar.",
        )

    if not plan.has_destination:
        return StatusFeedback(
            tone="error",
            message="Escolha uma pasta de destino para continuar.",
        )

    return StatusFeedback(
        tone="success",
        message=(
            f"Fluxo definido com sucesso para {plan.mode_label.lower()}. "
            f"Destino confirmado em {plan.destination}. "
            "Tudo pronto para iniciar o download."
        ),
    )


def start_download(plan: DownloadPlan) -> StatusFeedback:
    validation_feedback = build_review_status(plan)
    if validation_feedback.tone == "error":
        return validation_feedback

    try:
        Path(plan.destination).mkdir(parents=True, exist_ok=True)

        with YoutubeDL(_build_ydl_options(plan)) as downloader:
            downloader.download([plan.url])
    except DownloadError as error:
        return StatusFeedback(
            tone="error",
            message=f"Falha ao baixar o {plan.mode_label.lower()}: {error}",
        )
    except OSError as error:
        return StatusFeedback(
            tone="error",
            message=f"Nao foi possivel preparar a pasta de destino: {error}",
        )
    except Exception as error:
        return StatusFeedback(
            tone="error",
            message=f"Erro inesperado ao iniciar o download: {error}",
        )

    return StatusFeedback(
        tone="success",
        message=(
            f"Download de {plan.mode_label.lower()} iniciado e concluido em {plan.destination}."
        ),
    )


def _build_ydl_options(plan: DownloadPlan) -> dict[str, object]:
    output_template = str(Path(plan.destination) / "%(title)s.%(ext)s")

    if plan.mode == "audio":
        return {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

    return {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output_template,
        "noplaylist": True,
    }
