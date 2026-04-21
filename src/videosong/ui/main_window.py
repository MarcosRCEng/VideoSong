import tkinter as tk
from tkinter import filedialog, ttk

from src.videosong.services.download_service import (
    build_destination_label,
    build_download_checklist,
    build_download_plan,
    build_flow_summary,
    build_mode_guidance,
    build_review_status,
    build_review_button_label,
    build_url_guidance,
    start_download,
)


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("VideoSong")
        self.root.geometry("680x420")
        self.root.minsize(560, 360)

        self.url_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="video")
        self.destination_var = tk.StringVar()
        self.checklist_var = tk.StringVar()
        self.summary_var = tk.StringVar()
        self.url_guidance_var = tk.StringVar()
        self.mode_guidance_var = tk.StringVar()
        self.review_button_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Preencha a URL e escolha o formato para preparar o download.")
        self.selected_destination = ""
        self.status_label: ttk.Label | None = None

        self.url_var.trace_add("write", self._handle_form_change)
        self.mode_var.trace_add("write", self._handle_form_change)

        self._build()
        self._refresh_flow_summary()

    def _build(self) -> None:
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="VideoSong", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            container,
            text="Cole a URL, escolha entre video e audio e baixe sem complicacao.",
            wraplength=620,
        ).pack(anchor="w", pady=(4, 16))

        url_section = ttk.LabelFrame(container, text="1. URL do video", padding=16)
        url_section.pack(fill="x")

        ttk.Label(
            url_section,
            text="Cole o link do video que voce quer baixar.",
        ).pack(anchor="w")
        ttk.Entry(url_section, textvariable=self.url_var).pack(fill="x", pady=(8, 0))
        ttk.Label(
            url_section,
            textvariable=self.url_guidance_var,
            foreground="#555555",
            wraplength=620,
        ).pack(anchor="w", pady=(10, 0))

        mode_section = ttk.LabelFrame(container, text="2. Formato do download", padding=16)
        mode_section.pack(fill="x", pady=(16, 0))

        ttk.Label(
            mode_section,
            text="Escolha se o download vai manter o video completo ou somente o audio.",
            wraplength=620,
        ).pack(anchor="w")

        ttk.Radiobutton(
            mode_section,
            text="Video completo",
            value="video",
            variable=self.mode_var,
        ).pack(anchor="w", pady=(10, 0))
        ttk.Radiobutton(
            mode_section,
            text="Somente audio",
            value="audio",
            variable=self.mode_var,
        ).pack(anchor="w", pady=(6, 0))
        ttk.Label(
            mode_section,
            textvariable=self.mode_guidance_var,
            foreground="#555555",
            wraplength=620,
        ).pack(anchor="w", pady=(10, 0))

        destination_section = ttk.LabelFrame(container, text="3. Pasta de destino", padding=16)
        destination_section.pack(fill="x", pady=(16, 0))

        ttk.Label(
            destination_section,
            text="Escolha a pasta onde o arquivo sera salvo.",
            wraplength=620,
        ).pack(anchor="w")
        ttk.Button(destination_section, text="Escolher pasta", command=self._handle_choose_destination).pack(
            anchor="w", pady=(10, 0)
        )
        ttk.Label(
            destination_section,
            textvariable=self.destination_var,
            foreground="#555555",
            wraplength=620,
        ).pack(anchor="w", pady=(10, 0))

        ttk.Label(container, text="Checklist da preparacao").pack(anchor="w", pady=(16, 0))
        ttk.Label(container, textvariable=self.checklist_var, justify="left").pack(anchor="w", pady=(4, 0))

        ttk.Label(container, text="Resumo do fluxo").pack(anchor="w", pady=(16, 0))
        ttk.Label(container, textvariable=self.summary_var, wraplength=620).pack(anchor="w", pady=(4, 12))

        review_section = ttk.LabelFrame(container, text="4. Revisao final", padding=16)
        review_section.pack(fill="x")

        ttk.Label(
            review_section,
            text="Confira o resumo acima e inicie o download quando estiver tudo certo.",
            wraplength=620,
        ).pack(anchor="w")
        ttk.Button(review_section, textvariable=self.review_button_var, command=self._handle_download).pack(
            anchor="w", pady=(10, 0)
        )

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=16)
        ttk.Label(container, text="Status").pack(anchor="w")
        self.status_label = ttk.Label(container, textvariable=self.status_var, wraplength=620)
        self.status_label.pack(anchor="w", pady=(4, 0))

    def _handle_form_change(self, *_args: object) -> None:
        self._refresh_flow_summary()

    def _refresh_flow_summary(self) -> None:
        plan = build_download_plan(self.url_var.get(), self.mode_var.get(), self.selected_destination)
        self.summary_var.set(build_flow_summary(plan))
        self.destination_var.set(build_destination_label(plan))
        self.checklist_var.set(build_download_checklist(plan))
        self.url_guidance_var.set(build_url_guidance(plan))
        self.mode_guidance_var.set(build_mode_guidance(plan))
        self.review_button_var.set(build_review_button_label(plan))
        self._set_status("Preencha os itens pendentes e inicie o download quando estiver tudo certo.")

    def _handle_choose_destination(self) -> None:
        selected_directory = filedialog.askdirectory(title="Escolher pasta de destino")

        if not selected_directory:
            self._set_status(
                "Selecao de pasta cancelada. Escolha uma pasta para concluir a preparacao.",
                tone="error",
            )
            return

        self.selected_destination = selected_directory
        self._refresh_flow_summary()
        self._set_status("Pasta de destino definida. Revise o resumo e inicie o download.", tone="success")

    def _handle_download(self) -> None:
        plan = build_download_plan(self.url_var.get(), self.mode_var.get(), self.selected_destination)
        self._set_status("Iniciando download...", tone="info")
        self.root.update_idletasks()
        feedback = start_download(plan)
        self._set_status(feedback.message, tone=feedback.tone)

    def _set_status(self, message: str, tone: str = "info") -> None:
        self.status_var.set(message)

        if self.status_label is None:
            return

        colors = {
            "info": "#1f3a5f",
            "success": "#1f6b42",
            "error": "#9f2d2d",
        }
        self.status_label.configure(foreground=colors.get(tone, colors["info"]))

    def run(self) -> None:
        self.root.mainloop()
