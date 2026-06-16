import tkinter as tk
from tkinter import ttk

from ui.theme.tokens import BG, SURFACE, BORDER, PRIMARY, TEXT_PRIMARY, TEXT_SECONDARY


def setup_theme(root: tk.Tk):
    style = ttk.Style(root)
    style.theme_use("clam")

    root.configure(bg=BG)

    style.configure(
        "TFrame",
        background=BG
    )

    style.configure(
        "Card.TFrame",
        background=SURFACE,
        borderwidth=1,
        relief="solid"
    )

    style.configure(
        "TLabel",
        background=BG,
        foreground=TEXT_PRIMARY,
        font=("Segoe UI", 10)
    )

    style.configure(
        "PageHeader.TLabel",
        background=BG,
        foreground=TEXT_PRIMARY,
        font=("Segoe UI", 24, "bold")
    )

    style.configure(
        "Subtle.TLabel",
        background=BG,
        foreground=TEXT_SECONDARY,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview",
        background=SURFACE,
        fieldbackground=SURFACE,
        foreground=TEXT_PRIMARY,
        borderwidth=0,
        rowheight=28,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        background=SURFACE,
        foreground=PRIMARY,
        font=("Segoe UI", 10, "bold"),
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", BORDER)],
        foreground=[("selected", TEXT_PRIMARY)]
    )