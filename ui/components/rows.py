import tkinter as tk
from tkinter import ttk

def add_row(parent, label_text, variable, row):
    label = ttk.Label(parent, text=f"{label_text}:")
    label.grid(row=row, column=0, sticky="w", padx=(0, 20), pady=6)

    value = ttk.Label(parent, textvariable=variable, font=("Segoe UI", 10, "bold"))
    value.grid(row=row, column=1, sticky="w", pady=6)