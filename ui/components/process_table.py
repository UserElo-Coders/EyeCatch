import tkinter as tk
from tkinter import ttk

from ui.theme.tokens import SURFACE, BORDER


class ProcessTable(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=SURFACE,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        self.rows = []
        self.tree = None

    def render(self):
        self.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        container = tk.Frame(self, bg=SURFACE)
        container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            container,
            columns=("pid", "name", "cpu", "memory", "status"),
            show="headings",
            height=18
        )

        self.tree.heading("pid", text="PID")
        self.tree.heading("name", text="Process")
        self.tree.heading("cpu", text="CPU %")
        self.tree.heading("memory", text="Memory %")
        self.tree.heading("status", text="Status")

        self.tree.column("pid", width=70, anchor="center")
        self.tree.column("name", width=280)
        self.tree.column("cpu", width=80, anchor="center")
        self.tree.column("memory", width=90, anchor="center")
        self.tree.column("status", width=110, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update(self, processes):
        if self.tree is None:
            return

        processes = processes or []

        while len(self.rows) < len(processes):
            iid = self.tree.insert("", "end", values=("", "", "", "", ""))
            self.rows.append(iid)

        while len(self.rows) > len(processes):
            iid = self.rows.pop()
            self.tree.delete(iid)

        for i, proc in enumerate(processes):
            self.tree.item(
                self.rows[i],
                values=(
                    proc.pid,
                    proc.name,
                    f"{proc.cpu:.1f}",
                    f"{proc.memory:.1f}",
                    proc.status
                )
            )