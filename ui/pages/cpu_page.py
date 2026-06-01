import tkinter as tk
from tkinter import ttk

from ui.components.rows import add_row


class CPUPage:
    def __init__(self, content):
        self.content = content

        self.usage_var = tk.StringVar(value="--")
        self.temperature_var = tk.StringVar(value="--")
        self.frequency_var = tk.StringVar(value="--")
        self.cores_var = tk.StringVar(value="--")
        self.threads_var = tk.StringVar(value="--")

    def render(self, data):
        title = ttk.Label(self.content, text="CPU", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w", pady=(10, 15))

        self.card = ttk.Frame(self.content, padding=15, relief="ridge")
        self.card.pack(fill="both", expand=True)

        add_row(self.card, "Uso", self.usage_var, 0)
        add_row(self.card, "Temperatura", self.temperature_var, 1)
        add_row(self.card, "Frequência", self.frequency_var, 2)
        add_row(self.card, "Núcleos", self.cores_var, 3)
        add_row(self.card, "Threads", self.threads_var, 4)

        self.refresh(data)

    def refresh(self, data):
        if data is None:
            self.usage_var.set("--")
            self.temperature_var.set("--")
            self.frequency_var.set("--")
            self.cores_var.set("--")
            self.threads_var.set("--")
            return

        self.usage_var.set(f"{data.usage:.1f}%")
        self.temperature_var.set(data.temperature)
        self.frequency_var.set(data.frequency)
        self.cores_var.set(str(data.cores))
        self.threads_var.set(str(data.threads))