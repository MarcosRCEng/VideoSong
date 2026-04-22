from src.videosong.ui.main_window import MainWindow
from src.videosong.ui.url_list_manager import (
    EMPTY_URL_ERROR,
    INVALID_URL_ERROR,
    add_url,
    remove_url,
    validate_url_to_add,
)
from src.videosong.ui.wizard_messages import build_flow_summary, build_urls_label
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


class FakeListbox:
    def __init__(self, selection: tuple[int, ...] = ()) -> None:
        self.selection = selection
        self.items: list[str] = []

    def delete(self, _start: int, _end: object = None) -> None:
        self.items = []

    def insert(self, _index: object, value: str) -> None:
        self.items.append(value)

    def curselection(self) -> tuple[int, ...]:
        return self.selection


def make_window(*, urls: list[str] | None = None, destination: str = "C:/Downloads", mode: str = "video") -> MainWindow:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(urls=list(urls or []), mode=mode, destination=destination, active_step_index=2)
    window.current_url_var = FakeVar("")
    window.mode_var = FakeVar(mode)
    window.destination_var = FakeVar(destination)
    window.flow_var = FakeVar(build_flow_summary(window.state))
    window.urls_label_var = FakeVar(build_urls_label(window.state.urls))
    window.destination_label_var = FakeVar("")
    window.status_var = FakeVar("")
    window.status_label = FakeLabel()
    window.urls_listbox = FakeListbox()
    return window


def test_validate_url_to_add_rejects_blank_value() -> None:
    assert validate_url_to_add("   ") == EMPTY_URL_ERROR


def test_validate_url_to_add_rejects_invalid_url() -> None:
    assert validate_url_to_add("example.com/video") == INVALID_URL_ERROR


def test_add_url_appends_stripped_valid_url() -> None:
    urls, error = add_url(["https://example.com/a"], "  https://example.com/b  ")

    assert error is None
    assert urls == ["https://example.com/a", "https://example.com/b"]


def test_remove_url_ignores_out_of_range_index() -> None:
    assert remove_url(["https://example.com/a"], 10) == ["https://example.com/a"]


def test_handle_add_url_updates_state_and_listbox() -> None:
    window = make_window()
    window.current_url_var.set("https://example.com/watch?v=123")

    window._handle_add_url()

    assert window.state.urls == ["https://example.com/watch?v=123"]
    assert window.current_url_var.get() == ""
    assert window.urls_listbox.items == ["https://example.com/watch?v=123"]
    assert window.urls_label_var.get() == "1 URL(s) na lista atual."


def test_handle_add_url_reports_validation_error() -> None:
    window = make_window()
    window.current_url_var.set("url-invalida")

    window._handle_add_url()

    assert window.state.urls == []
    assert window.status_var.get() == INVALID_URL_ERROR
    assert window.status_label.fg == "#a12622"


def test_handle_remove_url_updates_state_and_listbox() -> None:
    window = make_window(urls=["https://example.com/a", "https://example.com/b"])
    window.urls_listbox = FakeListbox(selection=(0,))
    window._refresh_urls_listbox()

    window._handle_remove_url()

    assert window.state.urls == ["https://example.com/b"]
    assert window.urls_listbox.items == ["https://example.com/b"]
    assert window.urls_label_var.get() == "1 URL(s) na lista atual."


def test_handle_remove_url_requires_selection() -> None:
    window = make_window(urls=["https://example.com/a"])

    window._handle_remove_url()

    assert window.state.urls == ["https://example.com/a"]
    assert window.status_var.get() == "Erro: selecione uma URL da lista para remover."
