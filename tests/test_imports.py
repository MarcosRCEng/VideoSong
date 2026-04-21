from src.videosong.app import run
from src.videosong.ui.main_window import build_flow_summary, build_status_feedback, is_valid_url


def test_run_symbol_exists() -> None:
    assert callable(run)


def test_build_flow_summary_requires_url_first() -> None:
    assert build_flow_summary("", "video") == "Passo 1: cole a URL do video para liberar a validacao do fluxo."


def test_is_valid_url_accepts_http_and_https() -> None:
    assert is_valid_url("http://example.com")
    assert is_valid_url("https://example.com")
    assert not is_valid_url("example.com/video")


def test_build_flow_summary_requires_complete_url() -> None:
    assert (
        build_flow_summary("example.com/video", "video")
        == "Passo 1: use uma URL completa com http:// ou https:// para continuar."
    )


def test_build_status_feedback_returns_error_without_url() -> None:
    assert build_status_feedback("", "audio") == ("error", "Erro: informe uma URL antes de continuar.")


def test_build_status_feedback_returns_error_with_invalid_url() -> None:
    assert build_status_feedback("example.com/video", "audio") == (
        "error",
        "Erro: use uma URL valida com http:// ou https://.",
    )


def test_build_status_feedback_returns_success_with_url() -> None:
    status_kind, message = build_status_feedback("https://example.com/watch?v=123", "audio")

    assert status_kind == "success"
    assert "audio" in message
