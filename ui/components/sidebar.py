import tkinter as tk

from ui.theme.tokens import BACKGROUND, SURFACE, PRIMARY, TEXT_PRIMARY, TEXT_SECONDARY


class Sidebar(tk.Frame):
    def __init__(self, parent, navigate):
        super().__init__(parent, bg=BACKGROUND, width=240)
        self.pack_propagate(False)
        self.navigate = navigate
        self.buttons = {}

        tk.Label(
            self,
            text="USEREX",
            bg=BACKGROUND,
            fg=PRIMARY,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=24, pady=(30, 0))

        tk.Label(
            self,
            text="System Tracker",
            bg=BACKGROUND,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=24, pady=(0, 30))

        items = [
            ("Dashboard", "dashboard"),
            ("CPU", "cpu"),
            ("Memory", "ram"),
            ("Disk", "disk"),
            ("Network", "network"),
            ("Processes", "process"),
        ]

        for text, route in items:
            btn = tk.Button(
                self,
                text=text,
                command=lambda r=route: self.navigate(r),
                bg=SURFACE,
                fg=TEXT_PRIMARY,
                activebackground="#1D212B",
                activeforeground=TEXT_PRIMARY,
                relief="flat",
                bd=0,
                padx=20,
                pady=14,
                anchor="w",
                cursor="hand2",
                font=("Segoe UI", 11)
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.buttons[route] = btn

    def set_active(self, route):
        for name, btn in self.buttons.items():
            if name == route:
                btn.configure(bg="#1D212B", fg=PRIMARY)
            else:
                btn.configure(bg=SURFACE, fg=TEXT_PRIMARY)