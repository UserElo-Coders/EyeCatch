import tkinter as tk
from tkinter import ttk


class ProcessPage:
    def __init__(self, content, monitor):
        self.content = content
        self.monitor = monitor
        self.tree = None

    def render(self):
        title = ttk.Label(self.content, text="PROCESSES", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w", pady=(10, 15))

        container = ttk.Frame(self.content, padding=10)
        container.pack(fill="both", expand=True)

        columns = ("name", "pid", "cpu", "memory", "status")

        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=18)

        self.tree.heading("name", text="Processo")
        self.tree.heading("pid", text="PID")
        self.tree.heading("cpu", text="CPU %")
        self.tree.heading("memory", text="RAM %")
        self.tree.heading("status", text="Status")

        self.tree.column("name", width=280)
        self.tree.column("pid", width=80, anchor="center")
        self.tree.column("cpu", width=80, anchor="center")
        self.tree.column("memory", width=80, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh()

    def refresh(self):
        if self.tree is None:
            return

        processes = self.monitor.get_processes(limit=30)

        existing = self.tree.get_children()

        if len(existing) != len(processes):
            for item in existing:
                self.tree.delete(item)

            for p in processes:
                self.tree.insert(
                    "",
                    "end",
                    values=(p.name, p.pid, f"{p.cpu:.1f}", f"{p.memory:.1f}", p.status),
                )
            return

        for item, p in zip(existing, processes):
            self.tree.item(
                item,
                values=(p.name, p.pid, f"{p.cpu:.1f}", f"{p.memory:.1f}", p.status),
            )