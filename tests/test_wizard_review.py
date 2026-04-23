from src.videosong.ui.main_window import MainWindow
from src.videosong.services.download_queue import update_download_item
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


def test_build_review_summary_lists_format_destination_and_url_count() -> None:
    summary = build_review_summary(
        WizardState(
            urls=["https://example.com/a", "https://example.com/b"],
            mode="audio",
            destination="C:/Music",
            active_step_index=3,
        )
    )

    assert "Formato: Somente audio" in summary
    assert "Pasta de destino: C:/Music" in summary
    assert "Quantidade de URLs: 2" in summary
    assert "Estado: pronto para execucao." in summary
    assert "todas as URLs da fila serao processadas em ordem, uma por vez." in summary
    assert "1. https://example.com/a | Aguardando | Aguardando processamento." in summary
    assert "2. https://example.com/b | Aguardando | Aguardando processamento." in summary


def test_build_review_summary_marks_missing_required_data() -> None:
    summary = build_review_summary(WizardState(active_step_index=3))

    assert "Pasta de destino: Nao selecionada" in summary
    assert "Quantidade de URLs: 0" in summary
    assert "Estado: pendente, faltam a pasta de destino e a lista de URLs." in summary
    assert "Nenhum item na fila ainda." in summary


def test_build_review_summary_uses_live_download_items_when_provided() -> None:
    state = WizardState(
        urls=["https://example.com/very/long/path/that/needs/to/be/truncated/because/it/is/too/large"],
        mode="video",
        destination="C:/Downloads",
        active_step_index=3,
    )
    running_item = update_download_item(
        state.download_items[0],
        status="running",
        message="Baixando metadados do item.",
    )

    summary = build_review_summary(state, [running_item])

    assert "Baixando" in summary
    assert "Baixando metadados do item." in summary
    assert "..." in summary


def test_handle_next_blocks_advance_without_destination() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(active_step_index=1)
    window.status_var = FakeVar()
    window.status_label = FakeLabel()
    window._render_active_step = lambda: None

    window._handle_next()

    assert window.state.active_step_index == 1
    assert window.status_var.get() == "Escolha uma pasta de destino antes de avancar."
    assert window.status_label.fg == "#a12622"


def test_handle_next_blocks_advance_without_urls() -> None:
    window = MainWindow.__new__(MainWindow)
    window.state = WizardState(destination="C:/Downloads", active_step_index=2)
    window.status_var = FakeVar()
    window.status_label = FakeLabel()
    window._render_active_step = lambda: None

    window._handle_next()

    assert window.state.active_step_index == 2
    assert window.status_var.get() == "Adicione ao menos uma URL valida antes de avancar."
    assert window.status_label.fg == "#a12622"
