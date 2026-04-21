from src.videosong.app import run
from src.videosong.ui.main_window import build_destination_label, build_flow_summary, get_mode_details


def test_run_symbol_exists() -> None:
    assert callable(run)


def test_build_flow_summary_without_url() -> None:
    assert build_flow_summary("", "video", "") == "Cole uma URL para liberar a revisao do download."


def test_build_flow_summary_for_audio_mode() -> None:
    summary = build_flow_summary("https://example.com/watch?v=123", "audio", "")

    assert "modo audio" in summary
    assert "https://example.com/watch?v=123" in summary
    assert "Escolha a pasta de destino" in summary


def test_build_flow_summary_with_destination() -> None:
    summary = build_flow_summary("https://example.com/watch?v=123", "video", "C:/Downloads")

    assert "Pasta de destino: C:/Downloads" in summary


def test_build_destination_label_without_selection() -> None:
    assert build_destination_label("") == "Nenhuma pasta selecionada ainda."


def test_get_mode_details_defaults_to_video() -> None:
    assert get_mode_details("unexpected") == ("Video", "Baixar o video completo do link informado.")
