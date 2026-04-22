import json
from pathlib import Path
from uuid import uuid4

from src.videosong.services.settings_service import (
    get_last_destination,
    get_last_mode,
    load_settings,
    resolve_default_destination,
    save_settings,
    set_last_destination,
    set_last_mode,
)


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


def test_get_last_destination_returns_none_for_missing_or_invalid_value() -> None:
    assert get_last_destination({}) is None
    assert get_last_destination({"last_destination": ""}) is None
    assert get_last_destination({"last_destination": "   "}) is None
    assert get_last_destination({"last_destination": 123}) is None


def test_get_last_destination_returns_trimmed_saved_path() -> None:
    assert get_last_destination({"last_destination": "  C:/Downloads  "}) == "C:/Downloads"


def test_get_last_mode_returns_none_for_missing_or_invalid_value() -> None:
    assert get_last_mode({}) is None
    assert get_last_mode({"last_mode": ""}) is None
    assert get_last_mode({"last_mode": "mp3"}) is None
    assert get_last_mode({"last_mode": 123}) is None


def test_get_last_mode_returns_saved_video_or_audio_value() -> None:
    assert get_last_mode({"last_mode": "video"}) == "video"
    assert get_last_mode({"last_mode": "audio"}) == "audio"


def test_set_last_destination_updates_settings_copy_and_persists_with_load() -> None:
    test_directory = make_test_directory()
    settings_path = test_directory / "settings.json"
    original_settings = {"mode": "audio"}

    updated_settings = set_last_destination(original_settings, "  C:/Music  ")
    save_settings(updated_settings, settings_path)

    assert updated_settings == {"mode": "audio", "last_destination": "C:/Music"}
    assert original_settings == {"mode": "audio"}
    assert get_last_destination(load_settings(settings_path)) == "C:/Music"


def test_set_last_mode_updates_settings_copy_and_persists_with_load() -> None:
    test_directory = make_test_directory()
    settings_path = test_directory / "settings.json"
    original_settings = {"last_destination": "C:/Media"}

    updated_settings = set_last_mode(original_settings, " audio ")
    save_settings(updated_settings, settings_path)

    assert updated_settings == {"last_destination": "C:/Media", "last_mode": "audio"}
    assert original_settings == {"last_destination": "C:/Media"}
    assert get_last_mode(load_settings(settings_path)) == "audio"


def test_set_last_mode_ignores_unknown_modes() -> None:
    settings = {"last_destination": "C:/Media"}

    assert set_last_mode(settings, "playlist") == settings


def test_resolve_default_destination_prefers_videos_for_video_mode() -> None:
    test_directory = make_test_directory()
    videos_directory = test_directory / "Videos"
    videos_directory.mkdir()

    assert resolve_default_destination("video", test_directory) == str(videos_directory)


def test_resolve_default_destination_prefers_music_for_audio_mode() -> None:
    test_directory = make_test_directory()
    music_directory = test_directory / "Music"
    music_directory.mkdir()

    assert resolve_default_destination("audio", test_directory) == str(music_directory)


def test_resolve_default_destination_falls_back_to_home_when_preferred_folder_is_missing() -> None:
    test_directory = make_test_directory()

    assert resolve_default_destination("video", test_directory) == str(test_directory)
    assert resolve_default_destination("audio", test_directory) == str(test_directory)
