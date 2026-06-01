import tkinter as tk
from tkinter import ttk

from ui.components.rows import add_row


class DiskPage:
    def __init__(self, content):
        self.content = content

        self.usage_var = tk.StringVar(value="--")
        self.total_var = tk.StringVar(value="--")
        self.free_var = tk.StringVar(value="--")
        self.read_var = tk.StringVar(value="--")
        self.write_var = tk.StringVar(value="--")

    def render(self, data):
        title = ttk.Label(self.content, text="DISK", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w", pady=(10, 15))

        self.card = ttk.Frame(self.content, padding=15, relief="ridge")
        self.card.pack(fill="both", expand=True)

        add_row(self.card, "Uso", self.usage_var, 0)
        add_row(self.card, "Total", self.total_var, 1)
        add_row(self.card, "Livre", self.free_var, 2)
        add_row(self.card, "Leitura", self.read_var, 3)
        add_row(self.card, "Escrita", self.write_var, 4)

        self.refresh(data)

    def refresh(self, data):
        if data is None:
            self.usage_var.set("--")
            self.total_var.set("--")
            self.free_var.set("--")
            self.read_var.set("--")
            self.write_var.set("--")
            return

        self.usage_var.set(f"{data.usage:.1f}%")
        self.total_var.set(f"{data.total:.2f} GB")
        self.free_var.set(f"{data.free:.2f} GB")
        self.read_var.set(f"{data.read_speed:.2f} MB/s")
        self.write_var.set(f"{data.write_speed:.2f} MB/s")