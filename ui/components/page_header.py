import tkinter as tk
from ui.theme.tokens import BG, TEXT_PRIMARY, TEXT_SECONDARY


class PageHeader(tk.Frame):
    def __init__(self, parent, title: str, subtitle: str = ""):
        super().__init__(parent, bg=BG)
        self.pack(fill="x", padx=24, pady=(20, 12))

        tk.Label(
            self,
            text=title,
            bg=BG,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        if subtitle:
            tk.Label(
                self,
                text=subtitle,
                bg=BG,
                fg=TEXT_SECONDARY,
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=(4, 0))