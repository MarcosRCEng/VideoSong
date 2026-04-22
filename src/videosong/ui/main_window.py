import tkinter as tk
from collections.abc import Callable
from types import TracebackType
from tkinter import END, filedialog, ttk

from src.videosong.services.error_log import write_error_log
from src.videosong.services.download_service import start_download
from src.videosong.services.settings_service import resolve_default_destination
from src.videosong.ui.layout_metrics import (
    DEFAULT_WINDOW_GEOMETRY,
    DEFAULT_WINDOW_MINSIZE,
    calculate_wraplength,
)
from src.videosong.ui.url_batch_parser import (
    build_batch_feedback,
    parse_url_batch,
    validate_url_batch,
)
from src.videosong.ui.url_list_manager import add_url, remove_url
from src.videosong.ui.wizard_messages import (
    build_destination_label,
    build_flow_summary,
    build_urls_label,
)
from src.videosong.ui.wizard_review import (
    build_review_summary,
    build_status_feedback,
    can_advance_from_step,
    get_next_step_blocker,
)
from src.videosong.ui.wizard_state import WizardState
from src.videosong.ui.wizard_steps import WIZARD_STEPS, WizardStep


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("VideoSong")
        self.root.geometry(DEFAULT_WINDOW_GEOMETRY)
        self.root.minsize(*DEFAULT_WINDOW_MINSIZE)
        self.root.report_callback_exception = self._handle_tk_exception

        initial_mode = "video"
        initial_destination = resolve_default_destination(initial_mode)
        self.state = WizardState(mode=initial_mode, destination=initial_destination)
        self.current_url_var = tk.StringVar()
        self.mode_var = tk.StringVar(value=self.state.mode)
        self.destination_var = tk.StringVar(value=self.state.destination)
        self.step_title_var = tk.StringVar()
        self.step_description_var = tk.StringVar()
        self.step_progress_var = tk.StringVar()
        self.destination_label_var = tk.StringVar(value=build_destination_label(""))
        self.flow_var = tk.StringVar(value=build_flow_summary(self.state))
        self.review_summary_var = tk.StringVar(value=build_review_summary(self.state))
        self.urls_label_var = tk.StringVar(value=build_urls_label(self.state.urls))
        self.status_var = tk.StringVar(value="Status inicial: escolha o formato, defina a pasta e monte a lista de URLs.")
        self.status_color = "#1f1f1f"
        self.urls_listbox: tk.Listbox | None = None
        self.bulk_urls_text: tk.Text | None = None
        self._wrap_widgets: list[tuple[tk.Widget, int, int]] = []
        self._base_wrap_widgets_count = 0

        self._build()
        self.root.bind("<Configure>", self._handle_resize)
        self.mode_var.trace_add("write", self._handle_form_change)
        self.destination_var.trace_add("write", self._handle_form_change)
        self._render_active_step()

    def _build(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        container = ttk.Frame(self.root, padding=20)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(5, weight=1)

        ttk.Label(container, text="VideoSong", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(
            container,
            text="Fluxo em etapas preparado para evoluir a UI sem misturar estado, navegacao e execucao.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 16))

        ttk.Label(container, textvariable=self.step_progress_var, foreground="#555555").grid(
            row=2, column=0, sticky="w"
        )
        ttk.Label(container, textvariable=self.step_title_var).grid(row=3, column=0, sticky="w", pady=(8, 0))
        step_description_label = ttk.Label(container, textvariable=self.step_description_var, foreground="#555555")
        step_description_label.grid(row=4, column=0, sticky="ew", pady=(4, 16))
        self._register_wrap_widget(step_description_label, reserved_space=80, minimum=280)

        self.step_container = ttk.Frame(container)
        self.step_container.grid(row=5, column=0, sticky="nsew")
        self.step_container.columnconfigure(0, weight=1)
        self.step_container.rowconfigure(0, weight=1)

        navigation = ttk.Frame(container)
        navigation.grid(row=6, column=0, sticky="ew", pady=(12, 0))
        navigation.columnconfigure(2, weight=1)
        self.back_button = ttk.Button(navigation, text="Voltar", command=self._handle_back)
        self.back_button.grid(row=0, column=0, sticky="w")
        self.next_button = ttk.Button(navigation, text="Proximo", command=self._handle_next)
        self.next_button.grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.download_button = ttk.Button(navigation, text="Iniciar download", command=self._handle_download)
        self.download_button.grid(row=0, column=3, sticky="e")

        ttk.Separator(container, orient="horizontal").grid(row=7, column=0, sticky="ew", pady=16)
        ttk.Label(container, text="Status").grid(row=8, column=0, sticky="w")
        self.status_label = tk.Label(
            container,
            textvariable=self.status_var,
            justify="left",
            fg=self.status_color,
        )
        self.status_label.grid(row=9, column=0, sticky="ew", pady=(4, 0))
        self._register_wrap_widget(self.status_label, reserved_space=100, minimum=260)
        self._base_wrap_widgets_count = len(self._wrap_widgets)
        self._apply_wraplengths()

    def _handle_form_change(self, *_args: object) -> None:
        previous_mode = self.state.mode
        previous_destination = self.state.destination
        self._sync_state_from_vars()

        previous_default_destination = resolve_default_destination(previous_mode)
        current_default_destination = resolve_default_destination(self.state.mode)

        if previous_mode != self.state.mode and previous_destination.strip() == previous_default_destination:
            self.state.destination = current_default_destination
            if self.destination_var.get() != current_default_destination:
                self.destination_var.set(current_default_destination)

        self.flow_var.set(build_flow_summary(self.state))
        self.review_summary_var.set(build_review_summary(self.state))
        self.destination_label_var.set(build_destination_label(self.state.destination))
        self.urls_label_var.set(build_urls_label(self.state.urls))

    def _sync_state_from_vars(self) -> None:
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
        self._wrap_widgets = self._wrap_widgets[: self._base_wrap_widgets_count]

        for child in self.step_container.winfo_children():
            child.destroy()

        builders: dict[str, Callable[[ttk.Frame, WizardStep], None]] = {
            "format": self._build_format_step,
            "destination": self._build_destination_step,
            "urls": self._build_urls_step,
            "review": self._build_review_step,
        }
        builders[step.key](self.step_container, step)
        self._update_navigation_buttons()
        self._apply_wraplengths()

    def _build_format_step(self, parent: ttk.Frame, _step: WizardStep) -> None:
        parent.columnconfigure(0, weight=1)
        modes = ttk.Frame(parent)
        modes.grid(row=0, column=0, sticky="w", pady=(4, 12))
        ttk.Radiobutton(modes, text="Video completo", value="video", variable=self.mode_var).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(modes, text="Somente audio", value="audio", variable=self.mode_var).grid(
            row=0, column=1, sticky="w", padx=(16, 0)
        )
        helper_label = ttk.Label(
            parent,
            text="Escolha video para manter imagem e som, ou audio para extrair apenas a faixa sonora.",
            foreground="#555555",
        )
        helper_label.grid(row=1, column=0, sticky="ew")
        self._register_wrap_widget(helper_label, reserved_space=100, minimum=260)

    def _build_destination_step(self, parent: ttk.Frame, _step: WizardStep) -> None:
        parent.columnconfigure(0, weight=1)
        ttk.Button(parent, text="Escolher pasta", command=self._handle_choose_destination).grid(
            row=0, column=0, sticky="w", pady=(4, 8)
        )
        destination_label = ttk.Label(parent, textvariable=self.destination_label_var, foreground="#555555")
        destination_label.grid(row=1, column=0, sticky="ew")
        self._register_wrap_widget(destination_label, reserved_space=100, minimum=260)

    def _build_urls_step(self, parent: ttk.Frame, _step: WizardStep) -> None:
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(3, weight=1)

        input_row = ttk.Frame(parent)
        input_row.grid(row=0, column=0, sticky="ew", pady=(4, 8))
        input_row.columnconfigure(0, weight=1)
        ttk.Entry(input_row, textvariable=self.current_url_var).grid(row=0, column=0, sticky="ew")
        ttk.Button(input_row, text="Adicionar URL", command=self._handle_add_url).grid(row=0, column=1, sticky="e", padx=(8, 0))

        intro_label = ttk.Label(
            parent,
            text="Adicione manualmente uma URL por vez ou cole varias linhas com http:// ou https://.",
            foreground="#555555",
        )
        intro_label.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self._register_wrap_widget(intro_label, reserved_space=100, minimum=260)

        bulk_frame = ttk.Frame(parent)
        bulk_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 8))
        bulk_frame.columnconfigure(0, weight=1)
        self.bulk_urls_text = tk.Text(bulk_frame, height=4, wrap="word")
        self.bulk_urls_text.grid(row=0, column=0, sticky="ew")
        ttk.Button(bulk_frame, text="Adicionar em lote", command=self._handle_add_urls_batch).grid(
            row=0, column=1, sticky="ne", padx=(8, 0)
        )

        self.urls_listbox = tk.Listbox(parent, height=7, exportselection=False)
        self.urls_listbox.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
        self._refresh_urls_listbox()

        actions = ttk.Frame(parent)
        actions.grid(row=4, column=0, sticky="ew")
        actions.columnconfigure(1, weight=1)
        ttk.Button(actions, text="Remover selecionada", command=self._handle_remove_url).grid(row=0, column=0, sticky="w")
        ttk.Label(actions, textvariable=self.urls_label_var, foreground="#555555").grid(
            row=0, column=1, sticky="w", padx=(12, 0)
        )

    def _build_review_step(self, parent: ttk.Frame, _step: WizardStep) -> None:
        parent.columnconfigure(0, weight=1)
        ttk.Label(parent, text="Resumo do fluxo").grid(row=0, column=0, sticky="w")
        review_summary_label = ttk.Label(parent, textvariable=self.review_summary_var, justify="left")
        review_summary_label.grid(row=1, column=0, sticky="ew", pady=(4, 12))
        self._register_wrap_widget(review_summary_label, reserved_space=100, minimum=260)
        flow_label = ttk.Label(parent, textvariable=self.flow_var, foreground="#555555")
        flow_label.grid(row=2, column=0, sticky="ew")
        self._register_wrap_widget(flow_label, reserved_space=100, minimum=260)

    def _register_wrap_widget(self, widget: tk.Widget, reserved_space: int, minimum: int) -> None:
        self._wrap_widgets.append((widget, reserved_space, minimum))

    def _apply_wraplengths(self, width: int | None = None) -> None:
        root = getattr(self, "root", None)
        if root is None and width is None:
            return

        window_width = width or root.winfo_width()

        for widget, reserved_space, minimum in self._wrap_widgets:
            widget.configure(wraplength=calculate_wraplength(window_width, reserved_space, minimum))

    def _handle_resize(self, event: tk.Event[tk.Misc]) -> None:
        if event.widget is self.root:
            self._apply_wraplengths(width=event.width)

    def _update_navigation_buttons(self) -> None:
        self.back_button.configure(state="normal" if self.state.can_go_back() else "disabled")
        self.next_button.configure(state="normal" if self.state.can_go_next() and can_advance_from_step(self.state) else "disabled")
        self.download_button.configure(state="normal" if self.state.active_step.key == "review" else "disabled")

    def _handle_back(self) -> None:
        if self.state.go_back():
            self._render_active_step()

    def _handle_next(self) -> None:
        blocker = get_next_step_blocker(self.state)
        if blocker:
            self._set_status("error", blocker)
            return

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

    def _refresh_urls_listbox(self) -> None:
        if self.urls_listbox is None:
            return

        self.urls_listbox.delete(0, tk.END)
        for url in self.state.urls:
            self.urls_listbox.insert(tk.END, url)

    def _handle_add_url(self) -> None:
        updated_urls, error = add_url(self.state.urls, self.current_url_var.get())

        if error:
            self._set_status("error", error)
            return

        self.state.urls = updated_urls
        self.current_url_var.set("")
        self._handle_form_change()
        self._refresh_urls_listbox()
        self._set_status("neutral", f"URL adicionada. Lista atual com {len(self.state.urls)} item(ns).")

    def _handle_add_urls_batch(self) -> None:
        if self.bulk_urls_text is None:
            return

        batch_value = self.bulk_urls_text.get("1.0", END)
        validation_error = validate_url_batch(batch_value)

        if validation_error:
            self._set_status("error", validation_error)
            return

        result = parse_url_batch(batch_value, existing_urls=self.state.urls)
        status_kind, message = build_batch_feedback(result)

        if status_kind == "error":
            self._set_status(status_kind, message)
            return

        self.state.urls = [*self.state.urls, *result.accepted_urls]
        self.bulk_urls_text.delete("1.0", END)
        self._handle_form_change()
        self._refresh_urls_listbox()
        self._set_status(status_kind, f"{message} Lista atual com {len(self.state.urls)} item(ns).")

    def _handle_remove_url(self) -> None:
        if self.urls_listbox is None:
            return

        selection = self.urls_listbox.curselection()
        if not selection:
            self._set_status("error", "Erro: selecione uma URL da lista para remover.")
            return

        self.state.urls = remove_url(self.state.urls, selection[0])
        self._handle_form_change()
        self._refresh_urls_listbox()
        self._set_status("neutral", f"URL removida. Lista atual com {len(self.state.urls)} item(ns).")

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
        status_kind, message = start_download(self.state.primary_url, self.state.mode, self.state.destination)
        self._set_status(status_kind, message)

    def run(self) -> None:
        self.root.mainloop()
