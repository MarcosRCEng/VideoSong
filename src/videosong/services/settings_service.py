import json
from pathlib import Path
from typing import Any


DEFAULT_SETTINGS: dict[str, Any] = {}
LAST_DESTINATION_KEY = "last_destination"


def get_settings_file_path() -> Path:
    return Path.home() / ".videosong" / "settings.json"


def resolve_default_destination(mode: str, home_path: str | Path | None = None) -> str:
    base_home = Path(home_path) if home_path is not None else Path.home()
    preferred_directory_name = "Music" if mode == "audio" else "Videos"
    preferred_directory = base_home / preferred_directory_name

    if preferred_directory.is_dir():
        return str(preferred_directory)

    return str(base_home)


def get_last_destination(settings: dict[str, Any]) -> str | None:
    saved_destination = settings.get(LAST_DESTINATION_KEY)
    if not isinstance(saved_destination, str):
        return None

    normalized_destination = saved_destination.strip()
    if not normalized_destination:
        return None

    return normalized_destination


def set_last_destination(settings: dict[str, Any], destination: str) -> dict[str, Any]:
    updated_settings = dict(settings)
    updated_settings[LAST_DESTINATION_KEY] = destination.strip()
    return updated_settings


def load_settings(settings_path: str | Path | None = None) -> dict[str, Any]:
    file_path = Path(settings_path) if settings_path is not None else get_settings_file_path()

    try:
        raw_content = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return DEFAULT_SETTINGS.copy()

    try:
        loaded_settings = json.loads(raw_content)
    except json.JSONDecodeError:
        return DEFAULT_SETTINGS.copy()

    if not isinstance(loaded_settings, dict):
        return DEFAULT_SETTINGS.copy()

    return dict(loaded_settings)


def save_settings(settings: dict[str, Any], settings_path: str | Path | None = None) -> Path:
    file_path = Path(settings_path) if settings_path is not None else get_settings_file_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(settings, indent=2, sort_keys=True), encoding="utf-8")
    return file_path
