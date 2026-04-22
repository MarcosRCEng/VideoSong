from __future__ import annotations


DEFAULT_WINDOW_GEOMETRY = "860x620"
DEFAULT_WINDOW_MINSIZE = (640, 480)


def calculate_wraplength(window_width: int, reserved_space: int = 80, minimum: int = 260) -> int:
    """Return a wraplength that adapts to the current window width."""

    available_width = max(window_width - reserved_space, minimum)
    return available_width
