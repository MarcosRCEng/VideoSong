import tkinter as tk
from collections.abc import Callable
from types import TracebackType
from tkinter import filedialog, ttk

from src.videosong.services.error_log import write_error_log
from src.videosong.services.download_service import start_download
from src.videosong.ui.wizard_messages import (
    build_destination_label,
    build_flow_summary,
    build_status_feedback,
    is_valid_url,
)
from src.videosong.ui.wizard_state import WizardState
from src.videosong.ui.wizard_steps import WIZARD_STEPS, WizardStep


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("VideoSong")
        self.root.geometry("700x430")
        self.root.minsize(600, 380)
        self.root.report_callback_exception = self._handle_tk_exception

        self.state = WizardState()
        self.url_var = tk.StringVar(value=self.state.url)
        self.mode_var = tk.StringVar(value=self.state.mode)
        self.destination_var = tk.StringVar(value=self.state.destination)
        self.step_title_var = tk.StringVar()
        self.step_description_var = tk.StringVar()
        self.step_progress_var = tk.StringVar()
        self.destination_label_var = tk.StringVar(value=build_destination_label(""))
        self.flow_var = tk.StringVar(value=build_flow_summary(self.state))
        self.status_var = tk.StringVar(value="Status inicial: informe uma URL valida e confirme se quer video ou audio.")
        self.status_color = "#1f1f1f"

        self._build()
        self.url_var.trace_add("write", self._handle_form_change)
        self.mode_var.trace_add("write", self._handle_form_change)
        self.destination_var.trace_add("write", self._handle_form_change)
        self._render_active_step()

    def _build(self) -> None:
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="VideoSong", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            container,
            text="Fluxo em etapas preparado para evoluir a UI sem misturar estado, navegacao e execucao.",
        ).pack(anchor="w", pady=(4, 16))

        ttk.Label(container, textvariable=self.step_progress_var, foreground="#555555").pack(anchor="w")
        ttk.Label(container, textvariable=self.step_title_var).pack(anchor="w", pady=(8, 0))
        ttk.Label(container, textvariable=self.step_description_var, wraplength=620, foreground="#555555").pack(
            anchor="w", pady=(4, 16)
        )

        self.step_container = ttk.Frame(container)
        self.step_container.pack(fill="both", expand=True)

        navigation = ttk.Frame(container)
        navigation.pack(fill="x", pady=(12, 0))
        self.back_button = ttk.Button(navigation, text="Voltar", command=self._handle_back)
        self.back_button.pack(side="left")
        self.next_button = ttk.Button(navigation, text="Proximo", command=self._handle_next)
        self.next_button.pack(side="left", padx=(8, 0))
        self.download_button = ttk.Button(navigation, text="Iniciar download", command=self._handle_download)
        self.download_button.pack(side="right")

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=16)
        ttk.Label(container, text="Status").pack(anchor="w")
        self.status_label = tk.Label(
            container,
            textvariable=self.status_var,
            wraplength=600,
            justify="left",
            fg=self.status_color,
        )
        self.status_label.pack(anchor="w", pady=(4, 0))

    def _handle_form_change(self, *_args: object) -> None:
        self._sync_state_from_vars()
        self.flow_var.set(build_flow_summary(self.state))
        self.destination_label_var.set(build_destination_label(self.state.destination))

    def _sync_state_from_vars(self) -> None:
        self.state.url = self.url_var.get()
        self.state.mode = self.mode_var.get()
        self.state.destination = self.destination_var.get()

    def _build_step_progress(self) -> str:
        parts = [f"{step.index + 1}. {step.title.removeprefix(f'Passo {step.index + 1} - ')}" for step in WIZARD_STEPS]
        return "Etapas: " + "  |  ".join(parts)

    def _render_active_step(self) -> None:
        step = self.state.active_step
        self.step_progress_var.set(self._build_step_progress())
        self.step_title_var.set(step.title)
        self.step_description_var.set(step.description)

        for child in self.step_container.winfo_children():
            child.destroy()

        builders: dict[str, Callable[[ttk.Frame, WizardStep], None]] = {
            "url": self._build_url_step,
            "format": self._build_format_step,
            "destination": self._build_destination_step,
            "review": self._build_review_step,
        }
        builders[step.key](self.step_container, step)
        self._update_navigation_buttons()

    def _build_url_step(self, parent: ttk.Frame, _step: WizardStep) -> None:
        ttk.Entry(parent, textvariable=self.url_var).pack(fill="x", pady=(4, 12))
        ttk.Label(
            parent,
            text="Use uma URL completa, por exemplo: https://site.com/video",
            foreground="#555555",
            wraplength=620,
        ).pack(anchor="w")

    def _build_format_step(self, parent: ttk.Frame, _step: WizardStep) -> None:
        modes = ttk.Frame(parent)
        modes.pack(anchor="w", pady=(4, 12))
        ttk.Radiobutton(modes, text="Video completo", value="video", variable=self.mode_var).pack(side="left")
        ttk.Radiobutton(modes, text="Somente audio", value="audio", variable=self.mode_var).pack(side="left", padx=(16, 0))
        ttk.Label(
            parent,
            text="Escolha video para manter imagem e som, ou audio para extrair apenas a faixa sonora.",
            wraplength=620,
            foreground="#555555",
        ).pack(anchor="w")

    def _build_destination_step(self, parent: ttk.Frame, _step: WizardStep) -> None:
        ttk.Button(parent, text="Escolher pasta", command=self._handle_choose_destination).pack(anchor="w", pady=(4, 8))
        ttk.Label(parent, textvariable=self.destination_label_var, foreground="#555555", wraplength=620).pack(anchor="w")

    def _build_review_step(self, parent: ttk.Frame, _step: WizardStep) -> None:
        ttk.Label(parent, text="Resumo do fluxo").pack(anchor="w")
        ttk.Label(parent, textvariable=self.flow_var, wraplength=620).pack(anchor="w", pady=(4, 12))
        ttk.Label(parent, textvariable=self.destination_label_var, foreground="#555555", wraplength=620).pack(anchor="w")

    def _update_navigation_buttons(self) -> None:
        self.back_button.configure(state="normal" if self.state.can_go_back() else "disabled")
        self.next_button.configure(state="normal" if self.state.can_go_next() else "disabled")
        self.download_button.configure(state="normal" if self.state.active_step.key == "review" else "disabled")

    def _handle_back(self) -> None:
        if self.state.go_back():
            self._render_active_step()

    def _handle_next(self) -> None:
        if self.state.go_next():
            self._render_active_step()

    def _handle_choose_destination(self) -> None:
        selected_directory = filedialog.askdirectory(title="Escolher pasta de destino")

        if not selected_directory:
            self._set_status("neutral", "Selecao de pasta cancelada. Escolha um destino para concluir a preparacao.")
            return

        self.destination_var.set(selected_directory)
        self._handle_form_change()
        self._set_status("neutral", "Pasta de destino definida. Revise o resumo e valide o fluxo.")

    def _set_status(self, status_kind: str, message: str) -> None:
        colors = {
            "neutral": "#1f1f1f",
            "success": "#1f6f43",
            "error": "#a12622",
        }
        self.status_var.set(message)
        self.status_label.configure(fg=colors.get(status_kind, colors["neutral"]))

    def _handle_tk_exception(
        self,
        exc_type: type[BaseException],
        error: BaseException,
        traceback_obj: TracebackType | None,
    ) -> None:
        error.__traceback__ = traceback_obj
        log_file = write_error_log("Falha nao tratada na interface.", error)
        self._set_status(
            "error",
            f"Erro inesperado na interface. Consulte o log local em {log_file}.",
        )

    def _handle_download(self) -> None:
        self._sync_state_from_vars()
        status_kind, message = build_status_feedback(self.state)

        if status_kind == "error":
            self._set_status(status_kind, message)
            return

        self._set_status("neutral", "Iniciando download...")
        status_kind, message = start_download(self.state.url.strip(), self.state.mode, self.state.destination)
        self._set_status(status_kind, message)

    def run(self) -> None:
        self.root.mainloop()
