import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, parent, navigate):
        super().__init__(parent, bg="#0F1115", width=180)
        self.pack_propagate(False)

        tk.Label(self, text="EyeCatch", bg="#0F1115", fg="#E6EAF2",
                 font=("Segoe UI", 16, "bold")).pack(pady=20)

        buttons = [
            ("CPU", "cpu"),
            ("RAM", "ram"),
            ("DISK", "disk"),
            ("NET", "network"),
            ("PROC", "process")
        ]

        for text, route in buttons:
            tk.Button(
                self,
                text=text,
                command=lambda r=route: navigate(r),
                bg="#0F1115",
                fg="#8B93A7",
                relief="flat",
                anchor="w"
            ).pack(fill="x", padx=10, pady=5)