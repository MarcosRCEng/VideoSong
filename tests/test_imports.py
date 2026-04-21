from unittest.mock import MagicMock, patch

from yt_dlp import DownloadError

from src.videosong.app import run
from src.videosong.services.download_service import (
    build_destination_label,
    build_download_checklist,
    build_download_plan,
    build_flow_summary,
    build_mode_guidance,
    build_review_status,
    build_review_button_label,
    build_url_guidance,
    start_download,
)


def test_run_symbol_exists() -> None:
    assert callable(run)


def test_build_flow_summary_without_url() -> None:
    plan = build_download_plan("", "video", "")
    assert build_flow_summary(plan) == "Cole uma URL para liberar a revisao do download."


def test_build_flow_summary_for_audio_mode() -> None:
    plan = build_download_plan("https://example.com/watch?v=123", "audio", "")
    summary = build_flow_summary(plan)

    assert "modo audio" in summary
    assert "https://example.com/watch?v=123" in summary
    assert "Escolha a pasta de destino" in summary


def test_build_flow_summary_with_destination() -> None:
    plan = build_download_plan("https://example.com/watch?v=123", "video", "C:/Downloads")
    summary = build_flow_summary(plan)

    assert "Pasta de destino: C:/Downloads" in summary


def test_build_destination_label_without_selection() -> None:
    plan = build_download_plan("", "video", "")
    assert build_destination_label(plan) == "Nenhuma pasta selecionada ainda."


def test_build_url_guidance_without_url() -> None:
    plan = build_download_plan("", "video", "")
    assert build_url_guidance(plan) == "Cole a URL principal do video para liberar a proxima etapa."


def test_build_url_guidance_with_url() -> None:
    plan = build_download_plan("https://example.com/watch?v=123", "video", "")
    assert build_url_guidance(plan) == "URL pronta para uso: https://example.com/watch?v=123"


def test_build_mode_guidance_for_audio() -> None:
    plan = build_download_plan("https://example.com/watch?v=123", "audio", "")
    guidance = build_mode_guidance(plan)

    assert "Extrair somente o audio" in guidance
    assert "arquivo final sera salvo como audio" in guidance


def test_build_review_button_label_changes_with_mode() -> None:
    assert build_review_button_label(build_download_plan("", "video", "")) == "Baixar video"
    assert build_review_button_label(build_download_plan("", "audio", "")) == "Baixar audio"


def test_build_download_plan_defaults_to_video() -> None:
    plan = build_download_plan(" https://example.com ", "unexpected", " C:/Downloads ")

    assert plan.url == "https://example.com"
    assert plan.mode == "video"
    assert plan.destination == "C:/Downloads"


def test_build_download_checklist_marks_missing_steps() -> None:
    checklist = build_download_checklist(build_download_plan("", "audio", ""))

    assert "URL: pendente" in checklist
    assert "Formato: Audio" in checklist
    assert "Pasta: pendente" in checklist


def test_build_review_status_requires_url() -> None:
    feedback = build_review_status(build_download_plan("", "video", "C:/Downloads"))

    assert feedback.tone == "error"
    assert feedback.message == "Informe uma URL para continuar."


def test_build_review_status_requires_destination() -> None:
    feedback = build_review_status(build_download_plan("https://example.com/watch?v=123", "audio", ""))

    assert feedback.tone == "error"
    assert feedback.message == "Escolha uma pasta de destino para continuar."


def test_build_review_status_success_when_plan_is_ready() -> None:
    feedback = build_review_status(build_download_plan("https://example.com/watch?v=123", "audio", "C:/Downloads"))

    assert feedback.tone == "success"
    assert "Fluxo definido com sucesso para audio." in feedback.message
    assert "Tudo pronto para iniciar o download." in feedback.message


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_for_video_uses_ytdlp(mock_ytdl: MagicMock, mock_mkdir: MagicMock) -> None:
    downloader = MagicMock()
    mock_ytdl.return_value.__enter__.return_value = downloader

    feedback = start_download(build_download_plan("https://example.com/watch?v=123", "video", "C:/Downloads"))

    assert feedback.tone == "success"
    downloader.download.assert_called_once_with(["https://example.com/watch?v=123"])
    options = mock_ytdl.call_args.args[0]
    assert options["format"] == "bestvideo+bestaudio/best"
    mock_mkdir.assert_called_once()


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_for_audio_uses_postprocessor(mock_ytdl: MagicMock, _mock_mkdir: MagicMock) -> None:
    downloader = MagicMock()
    mock_ytdl.return_value.__enter__.return_value = downloader

    feedback = start_download(build_download_plan("https://example.com/watch?v=123", "audio", "C:/Downloads"))

    assert feedback.tone == "success"
    options = mock_ytdl.call_args.args[0]
    assert options["format"] == "bestaudio/best"
    assert options["postprocessors"][0]["key"] == "FFmpegExtractAudio"


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_returns_error_when_ytdlp_fails(mock_ytdl: MagicMock, _mock_mkdir: MagicMock) -> None:
    mock_ytdl.return_value.__enter__.side_effect = DownloadError("falha simulada")

    feedback = start_download(build_download_plan("https://example.com/watch?v=123", "video", "C:/Downloads"))

    assert feedback.tone == "error"
    assert "Falha ao baixar o video" in feedback.message
