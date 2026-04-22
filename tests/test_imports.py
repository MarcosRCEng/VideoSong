import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.videosong.app import run
from src.videosong.services.download_service import (
    DownloadError,
    build_download_options,
    find_ffmpeg_binary_path,
    find_ffmpeg_location,
    find_js_runtime_options,
    find_node_runtime_path,
    start_download,
)
from src.videosong.services.error_log import get_log_file_path, write_error_log
from src.videosong.ui import main_window
from src.videosong.ui.main_window import MainWindow
from src.videosong.ui.wizard_messages import build_destination_label, build_flow_summary, is_valid_url
from src.videosong.ui.wizard_review import build_review_summary, build_status_feedback
from src.videosong.ui.wizard_state import WizardState
from src.videosong.ui.wizard_steps import WIZARD_STEPS


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


class FakeButton:
    def __init__(self) -> None:
        self.state = None

    def configure(self, *, state: str) -> None:
        self.state = state


class FakeChild:
    def __init__(self) -> None:
        self.destroyed = False

    def destroy(self) -> None:
        self.destroyed = True


class FakeContainer:
    def __init__(self, children: list[FakeChild] | None = None) -> None:
        self.children = children or []

    def winfo_children(self) -> list[FakeChild]:
        return self.children


def test_run_symbol_exists() -> None:
    assert callable(run)


def test_get_log_file_path_points_to_project_logs_directory() -> None:
    log_file = get_log_file_path()

    assert log_file.name == "videosong-errors.log"
    assert log_file.parent.name == "logs"


def test_write_error_log_appends_context_and_error(monkeypatch) -> None:
    log_file = Path(f".tmp/test-videosong-errors-{os.getpid()}.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("src.videosong.services.error_log.get_log_file_path", lambda: log_file)

    saved_path = write_error_log("Falha de teste", RuntimeError("erro simulado"))

    assert saved_path == log_file
    content = log_file.read_text(encoding="utf-8")
    assert "Falha de teste" in content
    assert "erro simulado" in content


def test_wizard_state_starts_on_first_step() -> None:
    state = WizardState()

    assert state.active_step_index == 0
    assert state.active_step == WIZARD_STEPS[0]
    assert state.can_go_back() is False
    assert state.can_go_next() is True


def test_wizard_state_navigates_between_steps() -> None:
    state = WizardState()

    assert state.go_next() is True
    assert state.active_step == WIZARD_STEPS[1]
    assert state.go_back() is True
    assert state.active_step == WIZARD_STEPS[0]


def test_wizard_state_clamps_step_index() -> None:
    state = WizardState()

    state.set_active_step(999)
    assert state.active_step == WIZARD_STEPS[-1]

    state.set_active_step(-5)
    assert state.active_step == WIZARD_STEPS[0]


def test_build_flow_summary_requires_url_first() -> None:
    assert build_flow_summary(WizardState()) == "Passo 2: formato selecionado. Escolha a pasta de destino para concluir a preparacao."


def test_is_valid_url_accepts_http_and_https() -> None:
    assert is_valid_url("http://example.com")
    assert is_valid_url("https://example.com")
    assert not is_valid_url("example.com/video")


def test_is_valid_url_ignores_surrounding_spaces() -> None:
    assert is_valid_url("  https://example.com/watch?v=123  ")


def test_is_valid_url_rejects_blank_value() -> None:
    assert not is_valid_url("   ")


def test_build_flow_summary_requires_complete_url() -> None:
    state = WizardState(destination="C:/Downloads")

    assert (
        build_flow_summary(state)
        == "Passo 3: pasta definida em C:/Downloads. Adicione ao menos uma URL valida para liberar a revisao final."
    )


def test_build_flow_summary_requests_destination_before_completion() -> None:
    state = WizardState(mode="video")

    assert (
        build_flow_summary(state) == "Passo 2: formato selecionado. Escolha a pasta de destino para concluir a preparacao."
    )


def test_build_flow_summary_describes_audio_flow_with_destination() -> None:
    summary = build_flow_summary(
        WizardState(urls=["https://example.com/watch?v=123"], mode="audio", destination="C:/Downloads")
    )

    assert "formato audio" in summary
    assert "primeira URL da lista" in summary
    assert "https://example.com/watch?v=123" in summary


def test_build_destination_label_describes_selected_folder() -> None:
    assert build_destination_label("C:/Downloads") == "Pasta de destino: C:/Downloads"


def test_build_destination_label_requires_selection() -> None:
    assert build_destination_label("") == "Passo 2: escolha uma pasta de destino para concluir a preparacao do fluxo."


def test_build_status_feedback_returns_error_without_url() -> None:
    assert build_status_feedback(WizardState(mode="audio")) == (
        "error",
        "Erro: escolha uma pasta de destino antes de continuar.",
    )


def test_build_status_feedback_returns_error_with_invalid_url() -> None:
    assert build_status_feedback(WizardState(destination="C:/Downloads", mode="audio")) == (
        "error",
        "Erro: adicione ao menos uma URL valida antes de continuar.",
    )


def test_build_status_feedback_requires_destination() -> None:
    assert build_status_feedback(WizardState(urls=["https://example.com/watch?v=123"], mode="audio")) == (
        "error",
        "Erro: escolha uma pasta de destino antes de continuar.",
    )


def test_build_status_feedback_returns_success_with_url() -> None:
    status_kind, message = build_status_feedback(
        WizardState(urls=["https://example.com/watch?v=123"], mode="audio", destination="C:/Downloads")
    )

    assert status_kind == "success"
    assert "audio" in message
    assert "C:/Downloads" in message
    assert "primeira URL da lista" in message


def test_build_status_feedback_returns_success_for_video_mode() -> None:
    message = build_status_feedback(
        WizardState(urls=["https://example.com/watch?v=123"], mode="video", destination="C:/Media")
    )[1]

    assert "formato video" in message
    assert "C:/Media" in message


def test_handle_form_change_updates_wizard_state_and_summary() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState()
    window.mode_var = FakeVar("audio")
    window.destination_var = FakeVar("C:/Downloads")
    window.flow_var = FakeVar()
    window.review_summary_var = FakeVar()
    window.destination_label_var = FakeVar()
    window.urls_label_var = FakeVar()

    window._handle_form_change()

    assert window.state.mode == "audio"
    assert window.state.destination == "C:/Downloads"
    assert window.flow_var.get() == build_flow_summary(window.state)
    assert window.review_summary_var.get() == build_review_summary(window.state)
    assert window.destination_label_var.get() == build_destination_label("C:/Downloads")


def test_update_navigation_buttons_reflects_current_step() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(active_step_index=0)
    window.back_button = FakeButton()
    window.next_button = FakeButton()
    window.download_button = FakeButton()

    window._update_navigation_buttons()

    assert window.back_button.state == "disabled"
    assert window.next_button.state == "normal"
    assert window.download_button.state == "disabled"

    window.state = WizardState(
        urls=["https://example.com/watch?v=123"],
        destination="C:/Downloads",
        active_step_index=len(WIZARD_STEPS) - 1,
    )
    window._update_navigation_buttons()

    assert window.back_button.state == "normal"
    assert window.next_button.state == "disabled"
    assert window.download_button.state == "normal"


def test_update_navigation_buttons_blocks_next_without_required_data() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(active_step_index=1)
    window.back_button = FakeButton()
    window.next_button = FakeButton()
    window.download_button = FakeButton()

    window._update_navigation_buttons()

    assert window.back_button.state == "normal"
    assert window.next_button.state == "disabled"
    assert window.download_button.state == "disabled"


def test_handle_next_advances_step_and_rerenders() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState()
    rendered_steps: list[int] = []
    window._render_active_step = lambda: rendered_steps.append(window.state.active_step_index)

    window._handle_next()

    assert window.state.active_step_index == 1
    assert rendered_steps == [1]


def test_handle_back_returns_to_previous_step_and_rerenders() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(active_step_index=2)
    rendered_steps: list[int] = []
    window._render_active_step = lambda: rendered_steps.append(window.state.active_step_index)

    window._handle_back()

    assert window.state.active_step_index == 1
    assert rendered_steps == [1]


def test_render_active_step_updates_header_and_clears_previous_widgets() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(active_step_index=2)
    window.step_progress_var = FakeVar()
    window.step_title_var = FakeVar()
    window.step_description_var = FakeVar()
    old_child = FakeChild()
    window.step_container = FakeContainer(children=[old_child])
    window.back_button = FakeButton()
    window.next_button = FakeButton()
    window.download_button = FakeButton()
    called = {"builder": None}
    window._build_format_step = lambda *_args: called.update(builder="format")
    window._build_destination_step = lambda *_args: called.update(builder="destination")
    window._build_urls_step = lambda *_args: called.update(builder="urls")
    window._build_review_step = lambda *_args: called.update(builder="review")

    window._render_active_step()

    assert old_child.destroyed is True
    assert window.step_title_var.get() == "Passo 3 - Lista de URLs"
    assert "Etapas:" in window.step_progress_var.get()
    assert called["builder"] == "urls"


def test_handle_choose_destination_updates_folder_and_summary(monkeypatch) -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(mode="video")
    window.mode_var = FakeVar("video")
    window.destination_var = FakeVar("")
    window.destination_label_var = FakeVar("")
    window.flow_var = FakeVar("")
    window.review_summary_var = FakeVar("")
    window.urls_label_var = FakeVar("")
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
    window.state = WizardState(mode="video", destination="C:/Existing")
    window.mode_var = FakeVar("video")
    window.destination_var = FakeVar("C:/Existing")
    window.destination_label_var = FakeVar(build_destination_label("C:/Existing"))
    window.flow_var = FakeVar("resumo atual")
    window.review_summary_var = FakeVar(build_review_summary(window.state))
    window.urls_label_var = FakeVar("")
    window.status_var = FakeVar("")
    window.status_label = FakeLabel()

    monkeypatch.setattr(main_window.filedialog, "askdirectory", lambda title: "")

    window._handle_choose_destination()

    assert window.destination_var.get() == "C:/Existing"
    assert window.flow_var.get() == "resumo atual"
    assert window.status_var.get() == "Selecao de pasta cancelada. Escolha um destino para concluir a preparacao."


def test_build_download_options_for_video_uses_mp4_preference() -> None:
    with patch("src.videosong.services.download_service.find_ffmpeg_location", return_value="C:/ffmpeg/bin"):
        options = build_download_options("video", "C:/Downloads")

    assert options["format"] == "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
    assert options["merge_output_format"] == "mp4"
    assert options["ffmpeg_location"] == "C:/ffmpeg/bin"
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
    with patch("src.videosong.services.download_service.find_ffmpeg_location", return_value="C:/ffmpeg/bin"):
        options = build_download_options("audio", "C:/Downloads")

    assert options["format"] == "bestaudio/best"
    assert options["postprocessors"][0]["key"] == "FFmpegExtractAudio"
    assert options["postprocessors"][0]["preferredcodec"] == "mp3"
    assert options["ffmpeg_location"] == "C:/ffmpeg/bin"
    assert options["outtmpl"].endswith("\\%(title)s.%(ext)s")
    assert "Downloads" in options["outtmpl"]


@patch("src.videosong.services.download_service.which", return_value="C:/ffmpeg/bin/ffmpeg.exe")
def test_find_ffmpeg_binary_path_prefers_working_path_result(_mock_which: MagicMock) -> None:
    with patch(
        "src.videosong.services.download_service.is_working_ffmpeg_binary",
        side_effect=lambda path: str(path).replace("\\", "/") == "C:/ffmpeg/bin/ffmpeg.exe",
    ):
        assert str(find_ffmpeg_binary_path("ffmpeg")).replace("\\", "/") == "C:/ffmpeg/bin/ffmpeg.exe"


def test_find_ffmpeg_location_uses_shared_bin_folder() -> None:
    with patch(
        "src.videosong.services.download_service.find_ffmpeg_binary_path",
        side_effect=["C:/ffmpeg/bin/ffmpeg.exe", "C:/ffmpeg/bin/ffprobe.exe"],
    ):
        assert str(find_ffmpeg_location()).replace("\\", "/") == "C:/ffmpeg/bin"


def test_find_ffmpeg_location_returns_none_when_ffprobe_is_missing() -> None:
    with patch(
        "src.videosong.services.download_service.find_ffmpeg_binary_path",
        side_effect=["C:/ffmpeg/bin/ffmpeg.exe", None],
    ):
        assert find_ffmpeg_location() is None


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_calls_ytdlp(mock_ytdl: MagicMock, mock_mkdir: MagicMock) -> None:
    downloader = MagicMock()
    mock_ytdl.return_value.__enter__.return_value = downloader

    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        with patch("src.videosong.services.download_service.find_ffmpeg_location", return_value="C:/ffmpeg/bin"):
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
        with patch("src.videosong.services.download_service.find_ffmpeg_location", return_value="C:/ffmpeg/bin"):
            status_kind, _message = start_download("https://example.com/watch?v=123", "audio", "C:/Downloads")

    assert status_kind == "success"
    options = mock_ytdl.call_args.args[0]
    assert options["postprocessors"][0]["preferredcodec"] == "mp3"


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_returns_error_when_ytdlp_fails(mock_ytdl: MagicMock, _mock_mkdir: MagicMock) -> None:
    mock_ytdl.return_value.__enter__.side_effect = Exception("falha simulada")

    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        with patch("src.videosong.services.download_service.find_ffmpeg_location", return_value="C:/ffmpeg/bin"):
            with patch("src.videosong.services.download_service.write_error_log", return_value=Path("logs/videosong-errors.log")):
                status_kind, message = start_download("https://example.com/watch?v=123", "video", "C:/Downloads")

    assert status_kind == "error"
    assert "falha simulada" in message
    assert "videosong-errors.log" in message.replace("\\", "/")


@patch("src.videosong.services.download_service.Path.mkdir")
@patch("src.videosong.services.download_service.YoutubeDL")
def test_start_download_logs_download_error(mock_ytdl: MagicMock, _mock_mkdir: MagicMock) -> None:
    mock_ytdl.return_value.__enter__.side_effect = DownloadError("erro do yt-dlp")

    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        with patch("src.videosong.services.download_service.find_ffmpeg_location", return_value="C:/ffmpeg/bin"):
            with patch("src.videosong.services.download_service.write_error_log", return_value=Path("logs/videosong-errors.log")) as mock_log:
                status_kind, message = start_download("https://example.com/watch?v=123", "video", "C:/Downloads")

    assert status_kind == "error"
    assert "erro do yt-dlp" in message
    assert "videosong-errors.log" in message.replace("\\", "/")
    mock_log.assert_called_once()


def test_start_download_returns_guidance_for_youtube_without_js_runtime() -> None:
    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        status_kind, message = start_download("https://youtu.be/TdrL3QxjyVw", "video", "C:/Downloads")

    assert status_kind == "error"
    assert "nenhum runtime JavaScript compativel foi encontrado" in message
    assert "Node.js 20+" in message


def test_start_download_returns_guidance_when_ffmpeg_tools_are_missing() -> None:
    with patch("src.videosong.services.download_service.find_js_runtime_options", return_value={}):
        with patch("src.videosong.services.download_service.find_ffmpeg_location", return_value=None):
            status_kind, message = start_download("https://example.com/watch?v=123", "video", "C:/Downloads")

    assert status_kind == "error"
    assert "`ffmpeg` e `ffprobe` nao foram encontrados" in message


def test_handle_download_stops_when_validation_fails() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState()
    window.mode_var = FakeVar("video")
    window.destination_var = FakeVar("C:/Downloads")
    window.status_var = FakeVar()
    window.status_label = FakeLabel()

    window._handle_download()

    assert window.status_var.get() == "Erro: adicione ao menos uma URL valida antes de continuar."


def test_handle_download_uses_service_when_validation_passes(monkeypatch) -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(urls=["https://example.com/watch?v=123"])
    window.mode_var = FakeVar("audio")
    window.destination_var = FakeVar("C:/Downloads")
    window.status_var = FakeVar()
    window.status_label = FakeLabel()

    monkeypatch.setattr(main_window, "start_download", lambda url, mode, destination: ("success", f"baixado {mode} em {destination}"))

    window._handle_download()

    assert window.status_var.get() == "baixado audio em C:/Downloads"
    assert window.status_label.fg == "#1f6f43"


def test_handle_download_uses_first_url_from_list(monkeypatch) -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(urls=["https://example.com/first", "https://example.com/second"])
    window.mode_var = FakeVar("video")
    window.destination_var = FakeVar("C:/Downloads")
    window.status_var = FakeVar()
    window.status_label = FakeLabel()
    captured: dict[str, str] = {}

    def fake_start_download(url: str, mode: str, destination: str) -> tuple[str, str]:
        captured["url"] = url
        captured["mode"] = mode
        captured["destination"] = destination
        return ("success", "ok")

    monkeypatch.setattr(main_window, "start_download", fake_start_download)

    window._handle_download()

    assert captured == {
        "url": "https://example.com/first",
        "mode": "video",
        "destination": "C:/Downloads",
    }


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
