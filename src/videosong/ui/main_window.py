import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("VideoSong")
        self.root.geometry("640x320")
        self.root.minsize(520, 280)

        self.url_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="video")
        self.destination_var = tk.StringVar(value="Pasta de destino sera adicionada na proxima etapa.")
        self.status_var = tk.StringVar(value="Projeto inicial pronto para evoluir.")

        self._build()

    def _build(self) -> None:
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="VideoSong", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            container,
            text="Cole a URL do video, escolha o formato e acompanhe o status.",
        ).pack(anchor="w", pady=(4, 16))

        ttk.Label(container, text="URL do video").pack(anchor="w")
        ttk.Entry(container, textvariable=self.url_var).pack(fill="x", pady=(4, 12))

        ttk.Label(container, text="Modo de download").pack(anchor="w")
        modes = ttk.Frame(container)
        modes.pack(anchor="w", pady=(4, 12))
        ttk.Radiobutton(modes, text="Video", value="video", variable=self.mode_var).pack(side="left")
        ttk.Radiobutton(modes, text="Somente audio", value="audio", variable=self.mode_var).pack(
            side="left", padx=(16, 0)
        )

        ttk.Label(container, textvariable=self.destination_var, foreground="#555555").pack(anchor="w", pady=(0, 12))

        ttk.Button(container, text="Baixar", command=self._handle_download).pack(anchor="w")

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=16)
        ttk.Label(container, text="Status").pack(anchor="w")
        ttk.Label(container, textvariable=self.status_var, wraplength=560).pack(anchor="w", pady=(4, 0))

    def _handle_download(self) -> None:
        url = self.url_var.get().strip()

        if not url:
            self.status_var.set("Informe uma URL antes de iniciar o download.")
            return

        mode_label = "video" if self.mode_var.get() == "video" else "audio"
        self.status_var.set(
            f"Fluxo inicial validado. Proxima etapa: implementar o download real de {mode_label} para a URL informada."
        )

    def run(self) -> None:
        self.root.mainloop()
