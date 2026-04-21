from pathlib import Path

from yt_dlp import DownloadError, YoutubeDL


def build_download_options(mode: str, destination: str) -> dict[str, object]:
    output_template = str(Path(destination.strip()) / "%(title)s.%(ext)s")

    if mode == "audio":
        return {
            "format": "bestaudio/best",
            "noplaylist": True,
            "outtmpl": output_template,
        }

    return {
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
        "outtmpl": output_template,
    }


def start_download(url: str, mode: str, destination: str) -> tuple[str, str]:
    clean_url = url.strip()
    clean_mode = "audio" if mode == "audio" else "video"
    clean_destination = destination.strip()

    try:
        Path(clean_destination).mkdir(parents=True, exist_ok=True)

        with YoutubeDL(build_download_options(clean_mode, clean_destination)) as downloader:
            downloader.download([clean_url])
    except DownloadError as error:
        return ("error", f"Erro ao baixar {clean_mode}: {error}")
    except OSError as error:
        return ("error", f"Erro ao preparar a pasta de destino: {error}")
    except Exception as error:
        return ("error", f"Erro inesperado durante o download: {error}")

    return ("success", f"Download concluido com sucesso em {clean_destination}.")
