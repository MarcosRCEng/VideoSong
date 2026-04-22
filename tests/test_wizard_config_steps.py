from src.videosong.ui import main_window
from src.videosong.ui.main_window import MainWindow
from src.videosong.ui.wizard_messages import build_destination_label, build_flow_summary, build_urls_label
from src.videosong.ui.wizard_review import build_review_summary
from src.videosong.ui.wizard_state import WizardState


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


def make_window(
    *,
    url: str = "https://example.com/watch?v=123",
    mode: str = "video",
    destination: str = "",
    active_step_index: int = 0,
) -> MainWindow:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(
        urls=[url] if url else [],
        mode=mode,
        destination=destination,
        active_step_index=active_step_index,
    )
    window.current_url_var = FakeVar("")
    window.mode_var = FakeVar(mode)
    window.destination_var = FakeVar(destination)
    window.flow_var = FakeVar(build_flow_summary(window.state))
    window.review_summary_var = FakeVar(build_review_summary(window.state))
    window.destination_label_var = FakeVar(build_destination_label(destination))
    window.urls_label_var = FakeVar(build_urls_label(window.state.urls))
    window.status_var = FakeVar("")
    window.status_label = FakeLabel()
    window.urls_listbox = None
    window._render_active_step = lambda: None
    return window


def test_selected_format_persists_when_navigating_between_steps() -> None:
    window = make_window(active_step_index=0, mode="audio")

    window._handle_next()
    assert window.state.active_step_index == 1
    assert window.state.mode == "audio"

    window._handle_back()
    assert window.state.active_step_index == 0
    assert window.state.mode == "audio"
    assert window.mode_var.get() == "audio"


def test_destination_persists_after_returning_to_previous_step() -> None:
    window = make_window(active_step_index=1, destination="C:/Downloads")

    window._handle_back()
    assert window.state.active_step_index == 0
    assert window.state.destination == "C:/Downloads"

    window._handle_next()
    assert window.state.active_step_index == 1
    assert window.destination_var.get() == "C:/Downloads"
    assert window.state.destination == "C:/Downloads"


def test_choose_destination_updates_dedicated_step_state(monkeypatch) -> None:
    window = make_window(active_step_index=1, mode="audio")

    monkeypatch.setattr(main_window.filedialog, "askdirectory", lambda title: "C:/Music")

    window._handle_choose_destination()

    assert window.destination_var.get() == "C:/Music"
    assert window.state.destination == "C:/Music"
    assert window.destination_label_var.get() == "Pasta de destino: C:/Music"
    assert "C:/Music" in window.flow_var.get()


def test_choose_destination_keeps_existing_value_when_cancelled(monkeypatch) -> None:
    window = make_window(active_step_index=1, destination="C:/Existing")
    previous_summary = window.flow_var.get()

    monkeypatch.setattr(main_window.filedialog, "askdirectory", lambda title: "")

    window._handle_choose_destination()

    assert window.destination_var.get() == "C:/Existing"
    assert window.state.destination == "C:/Existing"
    assert window.flow_var.get() == previous_summary
    assert window.status_var.get() == "Selecao de pasta cancelada. Escolha um destino para concluir a preparacao."
