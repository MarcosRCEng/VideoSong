from src.videosong.app import run
from src.videosong.services.download_service import (
    build_destination_label,
    build_download_checklist,
    build_download_plan,
    build_flow_summary,
    build_review_status,
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
    assert "C:/Downloads" in feedback.message
