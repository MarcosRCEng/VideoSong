from __future__ import annotations

from dataclasses import dataclass, field

from src.videosong.services.download_queue import DownloadItem, build_download_queue
from src.videosong.ui.wizard_steps import WIZARD_STEPS, WizardStep


@dataclass(slots=True)
class WizardState:
    urls: list[str] = field(default_factory=list)
    mode: str = "video"
    destination: str = ""
    active_step_index: int = 0

    @property
    def active_step(self) -> WizardStep:
        return WIZARD_STEPS[self.active_step_index]

    @property
    def primary_url(self) -> str:
        if not self.urls:
            return ""

        return self.urls[0]

    @property
    def download_items(self) -> list[DownloadItem]:
        return build_download_queue(self.urls, self.mode, self.destination)

    def can_go_back(self) -> bool:
        return self.active_step_index > 0

    def can_go_next(self) -> bool:
        return self.active_step_index < len(WIZARD_STEPS) - 1

    def go_back(self) -> bool:
        if not self.can_go_back():
            return False

        self.active_step_index -= 1
        return True

    def go_next(self) -> bool:
        if not self.can_go_next():
            return False

        self.active_step_index += 1
        return True

    def set_active_step(self, index: int) -> None:
        bounded_index = max(0, min(index, len(WIZARD_STEPS) - 1))
        self.active_step_index = bounded_index
