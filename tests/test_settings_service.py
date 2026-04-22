import json
from pathlib import Path
from uuid import uuid4

from src.videosong.services.settings_service import load_settings, save_settings


def make_test_directory() -> Path:
    test_directory = Path(".tmp") / "tests" / f"settings-service-{uuid4().hex}"
    test_directory.mkdir(parents=True, exist_ok=True)
    return test_directory
def test_load_settings_returns_empty_dict_when_file_is_missing() -> None:
    test_directory = make_test_directory()
    settings_path = test_directory / "settings.json"

    assert load_settings(settings_path) == {}


def test_save_settings_writes_json_and_loads_saved_content() -> None:
    test_directory = make_test_directory()
    settings_path = test_directory / "nested" / "settings.json"
    settings = {"destination": "C:/Downloads", "mode": "audio"}

    saved_path = save_settings(settings, settings_path)

    assert saved_path == settings_path
    assert json.loads(settings_path.read_text(encoding="utf-8")) == settings
    assert load_settings(settings_path) == settings


def test_load_settings_falls_back_to_empty_dict_for_invalid_json() -> None:
    test_directory = make_test_directory()
    settings_path = test_directory / "settings.json"
    settings_path.write_text("{invalid json", encoding="utf-8")

    assert load_settings(settings_path) == {}
