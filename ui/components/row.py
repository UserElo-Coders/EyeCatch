import tkinter as tk
from ui.theme.tokens import CARD, TEXT, TEXT_MUTED


def Row(parent, label, value):
    frame = tk.Frame(parent, bg=CARD)
    frame.pack(fill="x", pady=6)

    tk.Label(frame, text=label, bg=CARD, fg=TEXT_MUTED).pack(side="left")
    tk.Label(frame, text=value, bg=CARD, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(side="right")