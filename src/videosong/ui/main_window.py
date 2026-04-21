import tkinter as tk
from tkinter import filedialog, ttk


def is_valid_url(value: str) -> bool:
    url = value.strip()
    return url.startswith("http://") or url.startswith("https://")


def build_destination_label(destination: str) -> str:
    clean_destination = destination.strip()

    if not clean_destination:
        return "Passo 3: escolha uma pasta de destino para concluir a preparacao do fluxo."

    return f"Pasta de destino: {clean_destination}"


def build_flow_summary(url: str, mode: str, destination: str) -> str:
    if not url.strip():
        return "Passo 1: cole a URL do video para liberar a validacao do fluxo."

    if not is_valid_url(url):
        return "Passo 1: use uma URL completa com http:// ou https:// para continuar."

    if not destination.strip():
        return "Passo 3: formato selecionado. Escolha a pasta de destino para concluir a preparacao."

    mode_label = "video" if mode == "video" else "audio"
    return (
        f"Passo 3: formato {mode_label} selecionado e pasta definida. "
        f"O fluxo esta pronto para seguir quando o download for integrado em {destination.strip()}."
    )


def build_status_feedback(url: str, mode: str, destination: str) -> tuple[str, str]:
    if not url.strip():
        return ("error", "Erro: informe uma URL antes de continuar.")

    if not is_valid_url(url):
        return ("error", "Erro: use uma URL valida com http:// ou https://.")

    if not destination.strip():
        return ("error", "Erro: escolha uma pasta de destino antes de continuar.")

    mode_label = "video" if mode == "video" else "audio"
    return (
        "success",
        (
            f"Fluxo validado: URL pronta, formato {mode_label} selecionado e destino definido em {destination.strip()}. "
            "A proxima etapa sera conectar o download real."
        ),
    )


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("VideoSong")
        self.root.geometry("700x430")
        self.root.minsize(600, 380)

        self.url_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="video")
        self.destination_var = tk.StringVar()
        self.destination_label_var = tk.StringVar(value=build_destination_label(""))
        self.flow_var = tk.StringVar(value=build_flow_summary("", self.mode_var.get(), self.destination_var.get()))
        self.status_var = tk.StringVar(value="Status inicial: informe uma URL valida e confirme se quer video ou audio.")
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
            text="Preencha a URL, escolha entre video completo ou somente audio e valide o fluxo antes da integracao do download.",
        ).pack(anchor="w", pady=(4, 16))

        instructions = ttk.Label(
            container,
            text="Fluxo atual: 1) URL  2) formato  3) validacao local. O download sera conectado em seguida.",
            wraplength=620,
        )
        instructions.pack(anchor="w", pady=(0, 16))

        ttk.Label(container, text="Passo 1 - URL do video").pack(anchor="w")
        ttk.Entry(container, textvariable=self.url_var).pack(fill="x", pady=(4, 12))
        ttk.Label(
            container,
            text="Use uma URL completa, por exemplo: https://site.com/video",
            foreground="#555555",
        ).pack(anchor="w", pady=(0, 12))

        ttk.Label(container, text="Passo 2 - Formato").pack(anchor="w")
        modes = ttk.Frame(container)
        modes.pack(anchor="w", pady=(4, 12))
        ttk.Radiobutton(modes, text="Video completo", value="video", variable=self.mode_var).pack(side="left")
        ttk.Radiobutton(modes, text="Somente audio", value="audio", variable=self.mode_var).pack(
            side="left", padx=(16, 0)
        )
        ttk.Label(
            container,
            text="Escolha video para manter imagem e som, ou audio para extrair apenas a faixa sonora.",
            wraplength=620,
            foreground="#555555",
        ).pack(anchor="w", pady=(0, 12))

        ttk.Label(container, text="Passo 3 - Pasta de destino").pack(anchor="w")
        ttk.Button(container, text="Escolher pasta", command=self._handle_choose_destination).pack(anchor="w", pady=(4, 8))
        ttk.Label(container, text="Resumo do fluxo").pack(anchor="w")
        ttk.Label(container, textvariable=self.flow_var, wraplength=600).pack(anchor="w", pady=(4, 12))

        ttk.Label(container, textvariable=self.destination_label_var, foreground="#555555", wraplength=600).pack(
            anchor="w", pady=(0, 12)
        )

        ttk.Button(container, text="Validar URL e formato", command=self._handle_download).pack(anchor="w")

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
        self.flow_var.set(build_flow_summary(self.url_var.get(), self.mode_var.get(), self.destination_var.get()))

    def _handle_choose_destination(self) -> None:
        selected_directory = filedialog.askdirectory(title="Escolher pasta de destino")

        if not selected_directory:
            self._set_status("neutral", "Selecao de pasta cancelada. Escolha um destino para concluir a preparacao.")
            return

        self.destination_var.set(selected_directory)
        self.destination_label_var.set(build_destination_label(selected_directory))
        self.flow_var.set(build_flow_summary(self.url_var.get(), self.mode_var.get(), selected_directory))
        self._set_status("neutral", "Pasta de destino definida. Revise o resumo e valide o fluxo.")

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
        status_kind, message = build_status_feedback(url, self.mode_var.get(), self.destination_var.get())
        self._set_status(status_kind, message)

    def run(self) -> None:
        self.root.mainloop()
