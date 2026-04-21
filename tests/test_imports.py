from src.videosong.app import run
from src.videosong.ui.main_window import MainWindow, build_flow_summary, build_status_feedback, is_valid_url


class FakeVar:
    def __init__(self, value: str = "") -> None:
        self.value = value

    def get(self) -> str:
        return self.value

    def set(self, value: str) -> None:
        self.value = value


class FakeLabel:
    def __init__(self) -> None:
        self.fg = None

    def configure(self, *, fg: str) -> None:
        self.fg = fg


def test_run_symbol_exists() -> None:
    assert callable(run)


def test_build_flow_summary_requires_url_first() -> None:
    assert build_flow_summary("", "video") == "Passo 1: cole a URL do video para liberar a validacao do fluxo."


def test_is_valid_url_accepts_http_and_https() -> None:
    assert is_valid_url("http://example.com")
    assert is_valid_url("https://example.com")
    assert not is_valid_url("example.com/video")


def test_is_valid_url_ignores_surrounding_spaces() -> None:
    assert is_valid_url("  https://example.com/watch?v=123  ")


def test_is_valid_url_rejects_blank_value() -> None:
    assert not is_valid_url("   ")


def test_build_flow_summary_requires_complete_url() -> None:
    assert (
        build_flow_summary("example.com/video", "video")
        == "Passo 1: use uma URL completa com http:// ou https:// para continuar."
    )


def test_build_flow_summary_describes_video_flow_when_valid() -> None:
    assert (
        build_flow_summary("https://example.com/watch?v=123", "video")
        == "Passo 2: formato video selecionado. O fluxo esta pronto para seguir quando o download for integrado."
    )


def test_build_flow_summary_describes_audio_flow_when_valid() -> None:
    assert (
        build_flow_summary("https://example.com/watch?v=123", "audio")
        == "Passo 2: formato audio selecionado. O fluxo esta pronto para seguir quando o download for integrado."
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


def test_build_status_feedback_returns_success_for_video_mode() -> None:
    assert build_status_feedback("https://example.com/watch?v=123", "video") == (
        "success",
        "Fluxo validado: URL pronta e formato video selecionado. A proxima etapa sera conectar o download real.",
    )


def test_handle_form_change_updates_flow_summary() -> None:
    window = MainWindow.__new__(MainWindow)
    window.url_var = FakeVar("https://example.com/watch?v=123")
    window.mode_var = FakeVar("audio")
    window.flow_var = FakeVar()

    window._handle_form_change()

    assert window.flow_var.get() == build_flow_summary("https://example.com/watch?v=123", "audio")


def test_set_status_updates_message_and_success_color() -> None:
    window = MainWindow.__new__(MainWindow)
    window.status_var = FakeVar()
    window.status_label = FakeLabel()

    window._set_status("success", "Fluxo validado.")

    assert window.status_var.get() == "Fluxo validado."
    assert window.status_label.fg == "#1f6f43"


def test_set_status_uses_neutral_color_for_unknown_status() -> None:
    window = MainWindow.__new__(MainWindow)
    window.status_var = FakeVar()
    window.status_label = FakeLabel()

    window._set_status("custom", "Mensagem neutra.")

    assert window.status_var.get() == "Mensagem neutra."
    assert window.status_label.fg == "#1f1f1f"
