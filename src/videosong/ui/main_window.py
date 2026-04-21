import tkinter as tk
from tkinter import ttk


def build_flow_summary(url: str, mode: str) -> str:
    if not url.strip():
        return "Passo 1: cole a URL para preparar o download."

    mode_label = "video" if mode == "video" else "audio"
    return f"Passo 2: formato {mode_label} selecionado. Revise e avance quando quiser."


def build_status_feedback(url: str, mode: str) -> tuple[str, str]:
    if not url.strip():
        return ("error", "Erro: informe uma URL antes de continuar.")

    mode_label = "video" if mode == "video" else "audio"
    return (
        "success",
        f"Sucesso: fluxo pronto para receber o download real de {mode_label} a partir da URL informada.",
    )


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("VideoSong")
        self.root.geometry("680x380")
        self.root.minsize(560, 340)

        self.url_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="video")
        self.destination_var = tk.StringVar(value="Pasta de destino sera adicionada na proxima etapa.")
        self.flow_var = tk.StringVar(value=build_flow_summary("", self.mode_var.get()))
        self.status_var = tk.StringVar(value="Status inicial: preencha a URL e escolha o formato.")
        self.status_color = "#1f1f1f"

        self._build()
        self.url_var.trace_add("write", self._handle_form_change)
        self.mode_var.trace_add("write", self._handle_form_change)

    def _build(self) -> None:
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="VideoSong", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            container,
            text="Cole a URL do video, escolha o formato e acompanhe o status do fluxo.",
        ).pack(anchor="w", pady=(4, 16))

        ttk.Label(container, text="Passo 1 - URL do video").pack(anchor="w")
        ttk.Entry(container, textvariable=self.url_var).pack(fill="x", pady=(4, 12))

        ttk.Label(container, text="Passo 2 - Formato").pack(anchor="w")
        modes = ttk.Frame(container)
        modes.pack(anchor="w", pady=(4, 12))
        ttk.Radiobutton(modes, text="Video", value="video", variable=self.mode_var).pack(side="left")
        ttk.Radiobutton(modes, text="Somente audio", value="audio", variable=self.mode_var).pack(
            side="left", padx=(16, 0)
        )

        ttk.Label(container, text="Resumo do fluxo").pack(anchor="w")
        ttk.Label(container, textvariable=self.flow_var, wraplength=600).pack(anchor="w", pady=(4, 12))

        ttk.Label(container, textvariable=self.destination_var, foreground="#555555").pack(anchor="w", pady=(0, 12))

        ttk.Button(container, text="Validar fluxo", command=self._handle_download).pack(anchor="w")

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
        self.flow_var.set(build_flow_summary(self.url_var.get(), self.mode_var.get()))

    def _set_status(self, status_kind: str, message: str) -> None:
        colors = {
            "neutral": "#1f1f1f",
            "success": "#1f6f43",
            "error": "#a12622",
        }
        self.status_var.set(message)
        self.status_label.configure(fg=colors.get(status_kind, colors["neutral"]))

    def _handle_download(self) -> None:
        url = self.url_var.get().strip()
        status_kind, message = build_status_feedback(url, self.mode_var.get())
        self._set_status(status_kind, message)

    def run(self) -> None:
        self.root.mainloop()
