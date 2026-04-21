from unittest.mock import MagicMock, patch

from src.videosong.app import run
from src.videosong.services.download_service import (
    build_download_options,
    find_js_runtime_options,
    find_node_runtime_path,
    start_download,
)
from src.videosong.ui import main_window
from src.videosong.ui.main_window import (
    MainWindow,
    build_destination_label,
    build_flow_summary,
    build_status_feedback,
    is_valid_url,
)


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
    assert build_flow_summary("", "video", "") == "Passo 1: cole a URL do video para liberar a validacao do fluxo."


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
        build_flow_summary("example.com/video", "video", "")
        == "Passo 1: use uma URL completa com http:// ou https:// para continuar."
    )


def test_build_flow_summary_requests_destination_before_completion() -> None:
    assert (
        build_flow_summary("https://example.com/watch?v=123", "video", "")
        == "Passo 3: formato selecionado. Escolha a pasta de destino para concluir a preparacao."
    )


def test_build_flow_summary_describes_audio_flow_with_destination() -> None:
    summary = build_flow_summary("https://example.com/watch?v=123", "audio", "C:/Downloads")

    assert "formato audio" in summary
    assert "C:/Downloads" in summary
    assert "iniciar o download" in summary


def test_build_destination_label_describes_selected_folder() -> None:
    assert build_destination_label("C:/Downloads") == "Pasta de destino: C:/Downloads"


def test_build_destination_label_requires_selection() -> None:
    assert build_destination_label("") == "Passo 3: escolha uma pasta de destino para concluir a preparacao do fluxo."


def test_build_status_feedback_returns_error_without_url() -> None:
    assert build_status_feedback("", "audio", "") == ("error", "Erro: informe uma URL antes de continuar.")


def test_build_status_feedback_returns_error_with_invalid_url() -> None:
    assert build_status_feedback("example.com/video", "audio", "") == (
        "error",
        "Erro: use uma URL valida com http:// ou https://.",
    )


def test_build_status_feedback_requires_destination() -> None:
    assert build_status_feedback("https://example.com/watch?v=123", "audio", "") == (
        "error",
        "Erro: escolha uma pasta de destino antes de continuar.",
    )


def test_build_status_feedback_returns_success_with_url() -> None:
    status_kind, message = build_status_feedback("https://example.com/watch?v=123", "audio", "C:/Downloads")

    assert status_kind == "success"
    assert "audio" in message
    assert "C:/Downloads" in message
    assert "Tudo pronto para iniciar o download." in message


def test_build_status_feedback_returns_success_for_video_mode() -> None:
    message = build_status_feedback("https://example.com/watch?v=123", "video", "C:/Media")[1]

    assert "formato video" in message
    assert "C:/Media" in message


def test_handle_form_change_updates_flow_summary() -> None:
    window = MainWindow.__new__(MainWindow)
    window.url_var = FakeVar("https://example.com/watch?v=123")
    window.mode_var = FakeVar("audio")
    window.destination_var = FakeVar("C:/Downloads")
    window.flow_var = FakeVar()

    window._handle_form_change()

    assert window.flow_var.get() == build_flow_summary("https://example.com/watch?v=123", "audio", "C:/Downloads")


def test_handle_choose_destination_updates_folder_and_summary(monkeypatch) -> None:
    window = MainWindow.__new__(MainWindow)
    window.url_var = FakeVar("https://example.com/watch?v=123")
    window.mode_var = FakeVar("video")
    window.destination_var = FakeVar("")
    window.destination_label_var = FakeVar("")
    window.flow_var = FakeVar("")
    window.status_var = FakeVar("")
    window.status_label = FakeLabel()

    monkeypatch.setattr(main_window.filedialog, "askdirectory", lambda title: "C:/Downloads")

    window._handle_choose_destination()

    assert window.destination_var.get() == "C:/Downloads"
    assert window.destination_label_var.get() == build_destination_label("C:/Downloads")
    assert "C:/Downloads" in window.flow_var.get()
    assert window.status_var.get() == "Pasta de destino definida. Revise o resumo e valide o fluxo."


def test_handle_choose_destination_keeps_destination_when_cancelled(monkeypatch) -> None:
    window = MainWindow.__new__(MainWindow)
    window.url_var = FakeVar("https://example.com/watch?v=123")
    window.mode_var = FakeVar("video")
    window.destination_var = FakeVar("C:/Existing")
    window.destination_label_var = FakeVar(build_destination_label("C:/Existing"))
    window.flow_var = FakeVar("resumo atual")
    window.status_var = FakeVar("")
    window.status_label = FakeLabel()

    monkeypatch.setattr(main_window.filedialog, "askdirectory", lambda title: "")

    window._handle_choose_destination()

    assert window.destination_var.get() == "C:/Existing"
    assert window.flow_var.get() == "resumo atual"
    assert window.status_var.get() == "Selecao de pasta cancelada. Escolha um destino para concluir a preparacao."


def test_build_download_options_for_video_uses_mp4_preference() -> None:
    options = build_download_options("video", "C:/Downloads")

    assert options["format"] == "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
    assert options["merge_output_format"] == "mp4"
    assert options["outtmpl"].endswith("\\%(title)s.%(ext)s")
    assert "Downloads" in options["outtmpl"]


@patch("src.videosong.services.download_service.which", return_value="C:/Runtime/node.exe")
def test_find_js_runtime_options_prefers_node_when_available(_mock_which: MagicMock) -> None:
    with patch("src.videosong.services.download_service.find_node_runtime_path", return_value="C:/Runtime/node.exe"):
        assert find_js_runtime_options() == {"node": {"path": "C:/Runtime/node.exe"}}


@patch("src.videosong.services.download_service.which", return_value=None)
def test_find_js_runtime_options_returns_empty_when_node_is_missing(_mock_which: MagicMock) -> None:
    with patch("src.videosong.services.download_service.find_node_runtime_path", return_value=None):
        assert find_js_runtime_options() == {}


@patch("src.videosong.services.download_service.which", return_value="C:/Runtime/node.exe")
def test_build_download_options_enables_node_runtime_when_available(_mock_which: MagicMock) -> None:
    with patch("src.videosong.services.download_service.find_node_runtime_path", return_value="C:/Runtime/node.exe"):
        options = build_download_options("video", "C:/Downloads")

        assert options["js_runtimes"] == {"node": {"path": "C:/Runtime/node.exe"}}


@patch("src.videosong.services.download_service.which", return_value="C:/Runtime/node.exe")
def test_find_node_runtime_path_prefers_working_path_result(_mock_which: MagicMock) -> None:
    with patch("src.videosong.services.download_service.is_working_node_runtime", side_effect=lambda path: path == "C:/Runtime/node.exe"):
        assert find_node_runtime_path() == "C:/Runtime/node.exe"


@patch("src.videosong.services.download_service.which", return_value="C:/WindowsApps/node.exe")
@patch.dict(
    "src.videosong.services.download_service.os.environ",
    {"ProgramFiles": "C:/Program Files", "LOCALAPPDATA": "C:/Users/Test/AppData/Local"},
    clear=False,
)
def test_find_node_runtime_path_falls_back_to_program_files_when_path_entry_is_not_usable(_mock_which: MagicMock) -> None:
    valid_path = "C:/Program Files/nodejs/node.exe"

    with patch(
        "src.videosong.services.download_service.is_working_node_runtime",
        side_effect=lambda path: str(path).replace("\\", "/") == valid_path,
    ):
        assert str(find_node_runtime_path()).replace("\\", "/") == valid_path


@patch("src.videosong.services.download_service.run")
def test_is_working_node_runtime_returns_true_for_version_output(mock_run: MagicMock) -> None:
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "v22.15.0"
    mock_run.return_value.stderr = ""

    from src.videosong.services.download_service import is_working_node_runtime

    assert is_working_node_runtime("C:/Runtime/node.exe") is True


@patch("src.videosong.services.download_service.run", side_effect=OSError("acesso negado"))
def test_is_working_node_runtime_returns_false_when_node_cannot_run(_mock_run: MagicMock) -> None:
    from src.videosong.services.download_service import is_working_node_runtime

    assert is_working_node_runtime("C:/Runtime/node.exe") is False


def test_build_download_options_for_audio_uses_mp3_postprocessor() -> None:
    options = build_download_options("audio", "C:/Downloads")

    assert options["format"] == "bestaudio/best"
    assert options["postprocessors"][0]["key"] == "FFmpegExtractAudio"
    assert options["postprocessors"][0]["preferredcodec"] == "mp3"
    assert options["outtmpl"].endswith("\\%(title)s.%(ext)s")
    assert "Downloads" in options["outtmpl"]


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_calls_ytdlp(mock_ytdl: MagicMock, mock_mkdir: MagicMock) -> None:
    downloader = MagicMock()
    mock_ytdl.return_value.__enter__.return_value = downloader

    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        status_kind, message = start_download("https://example.com/watch?v=123", "video", "C:/Downloads")

    assert status_kind == "success"
    assert "C:/Downloads" in message
    downloader.download.assert_called_once_with(["https://example.com/watch?v=123"])
    mock_mkdir.assert_called_once()
    options = mock_ytdl.call_args.args[0]
    assert options["merge_output_format"] == "mp4"


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_for_audio_uses_mp3_postprocessor(mock_ytdl: MagicMock, _mock_mkdir: MagicMock) -> None:
    downloader = MagicMock()
    mock_ytdl.return_value.__enter__.return_value = downloader

    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        status_kind, _message = start_download("https://example.com/watch?v=123", "audio", "C:/Downloads")

    assert status_kind == "success"
    options = mock_ytdl.call_args.args[0]
    assert options["postprocessors"][0]["preferredcodec"] == "mp3"


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_returns_error_when_ytdlp_fails(mock_ytdl: MagicMock, _mock_mkdir: MagicMock) -> None:
    mock_ytdl.return_value.__enter__.side_effect = Exception("falha simulada")

    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        status_kind, message = start_download("https://example.com/watch?v=123", "video", "C:/Downloads")

    assert status_kind == "error"
    assert "falha simulada" in message


def test_start_download_returns_guidance_for_youtube_without_js_runtime() -> None:
    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        status_kind, message = start_download("https://youtu.be/TdrL3QxjyVw", "video", "C:/Downloads")

    assert status_kind == "error"
    assert "nenhum runtime JavaScript compativel foi encontrado" in message
    assert "Node.js 20+" in message


def test_handle_download_stops_when_validation_fails() -> None:
    window = MainWindow.__new__(MainWindow)
    window.url_var = FakeVar("")
    window.mode_var = FakeVar("video")
    window.destination_var = FakeVar("C:/Downloads")
    window.status_var = FakeVar()
    window.status_label = FakeLabel()

    window._handle_download()

    assert window.status_var.get() == "Erro: informe uma URL antes de continuar."


def test_handle_download_uses_service_when_validation_passes(monkeypatch) -> None:
    window = MainWindow.__new__(MainWindow)
    window.url_var = FakeVar("https://example.com/watch?v=123")
    window.mode_var = FakeVar("audio")
    window.destination_var = FakeVar("C:/Downloads")
    window.status_var = FakeVar()
    window.status_label = FakeLabel()

    monkeypatch.setattr(main_window, "start_download", lambda url, mode, destination: ("success", f"baixado {mode} em {destination}"))

    window._handle_download()

    assert window.status_var.get() == "baixado audio em C:/Downloads"
    assert window.status_label.fg == "#1f6f43"


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
