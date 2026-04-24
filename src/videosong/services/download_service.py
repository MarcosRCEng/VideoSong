import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from subprocess import DEVNULL, run
from urllib.parse import urlparse

from yt_dlp import DownloadError, YoutubeDL

from src.videosong.services.error_log import write_error_log


@dataclass(frozen=True, slots=True)
class DownloadProgress:
    status: str
    percent: float | None
    speed: float | None
    eta: int | None
    elapsed: int | None


ProgressCallback = Callable[[DownloadProgress], None]


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


def is_working_ffmpeg_binary(binary_path: str | None) -> bool:
    if not binary_path:
        return False

    try:
        completed = run(
            [binary_path, "-version"],
            capture_output=True,
            text=True,
            check=False,
            stdin=DEVNULL,
        )
    except OSError:
        return False

    if completed.returncode != 0:
        return False

    version_output = f"{completed.stdout}{completed.stderr}".lower()
    return "ffmpeg version" in version_output or "ffprobe version" in version_output


def get_runtime_search_roots() -> list[str]:
    roots: list[str] = []

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        roots.append(str(Path(meipass)))

    executable_parent = Path(sys.executable).resolve().parent
    roots.append(str(executable_parent))
    roots.append(str(Path(__file__).resolve().parent))

    return list(dict.fromkeys(roots))


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


def find_ffmpeg_binary_path(binary_name: str) -> str | None:
    executable_name = f"{binary_name}.exe" if os.name == "nt" else binary_name
    bundled_candidates: list[str] = []

    for root in get_runtime_search_roots():
        bundled_candidates.extend(
            [
                os.path.join(root, executable_name),
                os.path.join(root, "ffmpeg", executable_name),
                os.path.join(root, "bin", executable_name),
            ]
        )

    candidates = [
        *bundled_candidates,
        which(binary_name),
        os.path.join(os.environ.get("ProgramFiles", ""), "ffmpeg", "bin", executable_name),
        os.path.join(os.environ.get("ProgramFiles", ""), "ffmpeg", executable_name),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Links", executable_name),
        os.path.join(os.environ.get("ChocolateyInstall", ""), "bin", executable_name),
    ]

    for candidate in candidates:
        if is_working_ffmpeg_binary(candidate):
            return candidate

    return None


def find_ffmpeg_location() -> str | None:
    ffmpeg_path = find_ffmpeg_binary_path("ffmpeg")
    ffprobe_path = find_ffmpeg_binary_path("ffprobe")

    if not ffmpeg_path or not ffprobe_path:
        return None

    ffmpeg_parent = str(Path(ffmpeg_path).parent)
    ffprobe_parent = str(Path(ffprobe_path).parent)

    if ffmpeg_parent == ffprobe_parent:
        return ffmpeg_parent

    return ffmpeg_path


def find_js_runtime_options() -> dict[str, dict[str, str]]:
    node_path = find_node_runtime_path()

    if not node_path:
        return {}

    return {"node": {"path": node_path}}


def _as_float(value: object) -> float | None:
    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    return None


def _as_int(value: object) -> int | None:
    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return int(value)

    return None


def build_download_progress(event: dict[str, object]) -> DownloadProgress | None:
    status = str(event.get("status", "")).strip()
    if status not in {"downloading", "finished"}:
        return None

    downloaded_bytes = _as_float(event.get("downloaded_bytes"))
    total_bytes = _as_float(event.get("total_bytes")) or _as_float(event.get("total_bytes_estimate"))
    percent = None
    if downloaded_bytes is not None and total_bytes and total_bytes > 0:
        percent = min(100.0, max(0.0, (downloaded_bytes / total_bytes) * 100))
    elif status == "finished":
        percent = 100.0

    return DownloadProgress(
        status=status,
        percent=percent,
        speed=_as_float(event.get("speed")),
        eta=_as_int(event.get("eta")),
        elapsed=_as_int(event.get("elapsed")),
    )


def build_download_options(
    mode: str,
    destination: str,
    progress_callback: ProgressCallback | None = None,
) -> dict[str, object]:
    output_template = str(Path(destination.strip()) / "%(title)s.%(ext)s")
    options: dict[str, object] = {
        "noplaylist": True,
        "outtmpl": output_template,
    }

    if progress_callback is not None:
        def progress_hook(event: dict[str, object]) -> None:
            progress = build_download_progress(event)
            if progress is not None:
                progress_callback(progress)

        options["progress_hooks"] = [progress_hook]

    js_runtimes = find_js_runtime_options()
    if js_runtimes:
        options["js_runtimes"] = js_runtimes

    ffmpeg_location = find_ffmpeg_location()
    if ffmpeg_location:
        options["ffmpeg_location"] = ffmpeg_location

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


def start_download(
    url: str,
    mode: str,
    destination: str,
    progress_callback: ProgressCallback | None = None,
) -> tuple[str, str]:
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

    if not find_ffmpeg_location():
        return (
            "error",
            (
                "Erro ao preparar o download: `ffmpeg` e `ffprobe` nao foram encontrados em um local utilizavel. "
                "Instale o pacote completo do FFmpeg e garanta que ambos estejam disponiveis no PATH antes de tentar novamente."
            ),
        )

    try:
        Path(clean_destination).mkdir(parents=True, exist_ok=True)

        with YoutubeDL(build_download_options(clean_mode, clean_destination, progress_callback)) as downloader:
            downloader.download([clean_url])
    except DownloadError as error:
        log_file = write_error_log("Falha de download retornada pelo yt-dlp.", error)
        return ("error", f"Erro ao baixar {clean_mode}: {error} Consulte o log em {log_file}.")
    except OSError as error:
        log_file = write_error_log("Falha ao preparar a pasta de destino.", error)
        return ("error", f"Erro ao preparar a pasta de destino: {error} Consulte o log em {log_file}.")
    except Exception as error:
        log_file = write_error_log("Falha inesperada durante o download.", error)
        return ("error", f"Erro inesperado durante o download: {error} Consulte o log em {log_file}.")

    return ("success", f"Download concluido com sucesso em {clean_destination}.")
