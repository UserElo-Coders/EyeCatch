import tkinter as tk
from tkinter import ttk

from ui.components.rows import add_row


class RAMPage:
    def __init__(self, content):
        self.content = content

        self.total_var = tk.StringVar(value="--")
        self.used_var = tk.StringVar(value="--")
        self.available_var = tk.StringVar(value="--")
        self.percent_var = tk.StringVar(value="--")
        self.cached_var = tk.StringVar(value="--")

    def render(self, data):
        title = ttk.Label(self.content, text="RAM", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w", pady=(10, 15))

        self.card = ttk.Frame(self.content, padding=15, relief="ridge")
        self.card.pack(fill="both", expand=True)

        add_row(self.card, "Total", self.total_var, 0)
        add_row(self.card, "Usada", self.used_var, 1)
        add_row(self.card, "Disponível", self.available_var, 2)
        add_row(self.card, "Uso", self.percent_var, 3)
        add_row(self.card, "Cache", self.cached_var, 4)

        self.refresh(data)

    def refresh(self, data):
        if data is None:
            self.total_var.set("--")
            self.used_var.set("--")
            self.available_var.set("--")
            self.percent_var.set("--")
            self.cached_var.set("--")
            return

        self.total_var.set(f"{data.total:.2f} GB")
        self.used_var.set(f"{data.used:.2f} GB")
        self.available_var.set(f"{data.available:.2f} GB")
        self.percent_var.set(f"{data.percent:.1f}%")
        self.cached_var.set(f"{data.cached:.2f} GB")