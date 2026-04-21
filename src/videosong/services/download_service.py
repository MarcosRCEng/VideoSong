import os
from pathlib import Path
from shutil import which
from subprocess import DEVNULL, run
from urllib.parse import urlparse

from yt_dlp import DownloadError, YoutubeDL


def is_youtube_url(url: str) -> bool:
    hostname = urlparse(url.strip()).hostname or ""
    hostname = hostname.lower()
    return hostname in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def is_working_node_runtime(node_path: str | None) -> bool:
    if not node_path:
        return False

    try:
        completed = run(
            [node_path, "--version"],
            capture_output=True,
            text=True,
            check=False,
            stdin=DEVNULL,
        )
    except OSError:
        return False

    if completed.returncode != 0:
        return False

    version_output = (completed.stdout or completed.stderr).strip()
    return version_output.startswith("v")


def find_node_runtime_path() -> str | None:
    candidates = [
        which("node"),
        os.path.join(os.environ.get("ProgramFiles", ""), "nodejs", "node.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "nodejs", "node.exe"),
    ]

    for candidate in candidates:
        if is_working_node_runtime(candidate):
            return candidate

    return None


def find_js_runtime_options() -> dict[str, dict[str, str]]:
    node_path = find_node_runtime_path()

    if not node_path:
        return {}

    return {"node": {"path": node_path}}


def build_download_options(mode: str, destination: str) -> dict[str, object]:
    output_template = str(Path(destination.strip()) / "%(title)s.%(ext)s")
    options: dict[str, object] = {
        "noplaylist": True,
        "outtmpl": output_template,
    }

    js_runtimes = find_js_runtime_options()
    if js_runtimes:
        options["js_runtimes"] = js_runtimes

    if mode == "audio":
        options.update(
            {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            }
        )
        return options

    options.update(
        {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        }
    )
    return options


def start_download(url: str, mode: str, destination: str) -> tuple[str, str]:
    clean_url = url.strip()
    clean_mode = "audio" if mode == "audio" else "video"
    clean_destination = destination.strip()
    js_runtimes = find_js_runtime_options()

    if is_youtube_url(clean_url) and not js_runtimes:
        return (
            "error",
            (
                "Erro ao preparar o download do YouTube: nenhum runtime JavaScript compativel foi encontrado. "
                "Instale Node.js 20+ e garanta que `node` esteja disponivel no PATH antes de tentar novamente."
            ),
        )

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
