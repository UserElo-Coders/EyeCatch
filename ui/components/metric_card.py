import tkinter as tk
from ui.theme.tokens import SURFACE, BORDER, TEXT_PRIMARY, TEXT_SECONDARY


class MetricCard(tk.Frame):
    def __init__(self, parent, title: str, variable: tk.StringVar):
        super().__init__(
            parent,
            bg=SURFACE,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        self.columnconfigure(0, weight=1)

        tk.Label(
            self,
            text=title,
            bg=SURFACE,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 0))

        tk.Label(
            self,
            textvariable=variable,
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 24, "bold")
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(10, 18))