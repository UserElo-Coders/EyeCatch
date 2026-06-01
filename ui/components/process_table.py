import tkinter as tk
from ui.theme.tokens import CARD, TEXT, TEXT_MUTED


class ProcessTable(tk.Frame):
    def __init__(self, parent, processes):
        super().__init__(parent, bg=CARD)
        self.pack(fill="both", expand=True)

        self.processes = processes

        # define grid estrutura global
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=2)

        self._build_header()
        self._build_rows()

    def _build_header(self):
        headers = ["PID", "NAME", "CPU", "RAM", "STATUS"]

        for col, text in enumerate(headers):
            tk.Label(
                self,
                text=text,
                bg=CARD,
                fg=TEXT_MUTED,
                font=("Segoe UI", 10, "bold"),
                anchor="w"
            ).grid(row=0, column=col, sticky="ew", padx=6, pady=(5, 10))

    def _build_rows(self):
        for i, p in enumerate(self.processes[:25], start=1):

            tk.Label(self, text=str(p.pid),
                     bg=CARD, fg=TEXT,
                     anchor="w").grid(row=i, column=0, sticky="ew", padx=6)

            tk.Label(self, text=(p.name[:25] if p.name else "Unknown"),
                     bg=CARD, fg=TEXT,
                     anchor="w").grid(row=i, column=1, sticky="ew", padx=6)

            tk.Label(self, text=f"{p.cpu:.1f}%",
                     bg=CARD, fg=TEXT,
                     anchor="w").grid(row=i, column=2, sticky="ew", padx=6)

            tk.Label(self, text=f"{p.memory:.1f}%",
                     bg=CARD, fg=TEXT,
                     anchor="w").grid(row=i, column=3, sticky="ew", padx=6)

            tk.Label(self, text=p.status,
                     bg=CARD, fg=TEXT_MUTED,
                     anchor="w").grid(row=i, column=4, sticky="ew", padx=6)