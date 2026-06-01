import tkinter as tk
from tkinter import ttk

from ui.components.rows import add_row


class NetworkPage:
    def __init__(self, content):
        self.content = content

        self.sent_speed_var = tk.StringVar(value="--")
        self.received_speed_var = tk.StringVar(value="--")
        self.total_sent_var = tk.StringVar(value="--")
        self.total_received_var = tk.StringVar(value="--")

    def render(self, data):
        title = ttk.Label(self.content, text="NETWORK", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w", pady=(10, 15))

        self.card = ttk.Frame(self.content, padding=15, relief="ridge")
        self.card.pack(fill="both", expand=True)

        add_row(self.card, "Upload", self.sent_speed_var, 0)
        add_row(self.card, "Download", self.received_speed_var, 1)
        add_row(self.card, "Total enviado", self.total_sent_var, 2)
        add_row(self.card, "Total recebido", self.total_received_var, 3)

        self.refresh(data)

    def refresh(self, data):
        if data is None:
            self.sent_speed_var.set("--")
            self.received_speed_var.set("--")
            self.total_sent_var.set("--")
            self.total_received_var.set("--")
            return

        self.sent_speed_var.set(f"{data.sent_speed:.2f} KB/s")
        self.received_speed_var.set(f"{data.received_speed:.2f} KB/s")
        self.total_sent_var.set(f"{data.total_sent / (1024 ** 2):.2f} MB")
        self.total_received_var.set(f"{data.total_received / (1024 ** 2):.2f} MB")