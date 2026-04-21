import tkinter as tk
from tkinter import ttk


def get_mode_details(mode: str) -> tuple[str, str]:
    if mode == "audio":
        return ("Audio", "Extrair somente o audio do link informado.")

    return ("Video", "Baixar o video completo do link informado.")


def build_flow_summary(url: str, mode: str) -> str:
    clean_url = url.strip()
    mode_label, mode_description = get_mode_details(mode)

    if not clean_url:
        return "Cole uma URL para liberar a revisao do download."

    return f"Pronto para baixar em modo {mode_label.lower()}: {clean_url}. {mode_description}"


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("VideoSong")
        self.root.geometry("680x420")
        self.root.minsize(560, 360)

        self.url_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="video")
        self.destination_var = tk.StringVar(value="Pasta de destino sera escolhida na proxima etapa.")
        self.summary_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Preencha a URL e escolha o formato para preparar o download.")

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
            text="Cole a URL, escolha entre video e audio e deixe o download pronto para a proxima etapa.",
            wraplength=620,
        ).pack(anchor="w", pady=(4, 16))

        url_section = ttk.LabelFrame(container, text="1. URL do video", padding=16)
        url_section.pack(fill="x")

        ttk.Label(
            url_section,
            text="Cole o link do video que voce quer baixar.",
        ).pack(anchor="w")
        ttk.Entry(url_section, textvariable=self.url_var).pack(fill="x", pady=(8, 0))

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

        ttk.Label(container, text="Resumo do fluxo").pack(anchor="w", pady=(16, 0))
        ttk.Label(container, textvariable=self.summary_var, wraplength=620).pack(anchor="w", pady=(4, 12))

        ttk.Label(container, textvariable=self.destination_var, foreground="#555555", wraplength=620).pack(
            anchor="w", pady=(0, 12)
        )

        ttk.Button(container, text="Preparar download", command=self._handle_download).pack(anchor="w")

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=16)
        ttk.Label(container, text="Status").pack(anchor="w")
        ttk.Label(container, textvariable=self.status_var, wraplength=620).pack(anchor="w", pady=(4, 0))

    def _handle_form_change(self, *_args: object) -> None:
        self._refresh_flow_summary()

    def _refresh_flow_summary(self) -> None:
        self.summary_var.set(build_flow_summary(self.url_var.get(), self.mode_var.get()))

    def _handle_download(self) -> None:
        url = self.url_var.get().strip()

        if not url:
            self.status_var.set("Informe uma URL para continuar.")
            return

        mode_label, mode_description = get_mode_details(self.mode_var.get())
        self.status_var.set(
            f"Fluxo definido com sucesso. Proxima etapa: conectar o download de {mode_label.lower()}. "
            f"{mode_description}"
        )

    def run(self) -> None:
        self.root.mainloop()
