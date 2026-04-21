from src.videosong.app import run
from src.videosong.ui.main_window import build_flow_summary, build_status_feedback


def test_run_symbol_exists() -> None:
    assert callable(run)


def test_build_flow_summary_requires_url_first() -> None:
    assert build_flow_summary("", "video") == "Passo 1: cole a URL para preparar o download."


def test_build_status_feedback_returns_error_without_url() -> None:
    assert build_status_feedback("", "audio") == ("error", "Erro: informe uma URL antes de continuar.")


def test_build_status_feedback_returns_success_with_url() -> None:
    status_kind, message = build_status_feedback("https://example.com/watch?v=123", "audio")

    assert status_kind == "success"
    assert "audio" in message
