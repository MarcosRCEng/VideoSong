from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import traceback


def get_log_file_path() -> Path:
    if getattr(sys, "frozen", False):
        base_path = Path(sys.executable).resolve().parent
    else:
        base_path = Path(__file__).resolve().parents[3]

    log_directory = base_path / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)
    return log_directory / "videosong-errors.log"


def write_error_log(context: str, error: BaseException) -> Path:
    log_file = get_log_file_path()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stack_trace = "".join(traceback.format_exception(type(error), error, error.__traceback__)).strip()

    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {context}\n{stack_trace}\n\n")

    return log_file
