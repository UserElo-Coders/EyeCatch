import tkinter as tk
from ui.theme.tokens import CARD, BORDER


class Card(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        self.pack(fill="both", expand=True, padx=20, pady=15)