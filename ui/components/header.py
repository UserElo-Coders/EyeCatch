import tkinter as tk
from ui.theme.tokens import BG, TEXT, TEXT_MUTED


class Header(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, bg=BG)
        self.pack(fill="x", padx=20, pady=10)

        tk.Label(self, text=title, bg=BG, fg=TEXT, font=("Segoe UI", 18, "bold")).pack(anchor="w")