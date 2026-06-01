import tkinter as tk
from tkinter import ttk
from core.monitor import SystemMonitor

class DashboardApp:
    def __init__(self, root: tk.Tk, monitor: SystemMonitor):
        self.root = root
        self.monitor = monitor

        self.root.title("UserEx Monitor")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        self.usage_var = tk.StringVar(value="--")
        self.temperature_var = tk.StringVar(value="--")
        self.frequency_var = tk.StringVar(value="--")
        self.cores_var = tk.StringVar(value="--")
        self.threads_var = tk.StringVar(value="--")

        self.ram_total_var = tk.StringVar(value="--")
        self.ram_used_var = tk.StringVar(value="--")
        self.ram_available_var = tk.StringVar(value="--")
        self.ram_percent_var = tk.StringVar(value="--")
        self.ram_cached_var = tk.StringVar(value="--")

        self._build_ui()
        self.update_cpu()
        self.update_ram()

    def _build_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar = ttk.Frame(self.main_frame, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content = ttk.Frame(self.main_frame)
        self.content.pack(side="right", fill="both", expand=True)

        ttk.Button(
            self.sidebar,
            text="CPU",
            command=self.show_cpu
        ).pack(fill="x", padx=10, pady=5)

        ttk.Button(
            self.sidebar,
            text="RAM",
            command=self.show_ram
        ).pack(fill="x", padx=10, pady=5)

        self.show_cpu()

    def _add_row(self, parent, label_text, variable, row):
        label = ttk.Label(parent, text=label_text + ":")
        label.grid(row=row, column=0, sticky="w", padx=(0, 20), pady=6)

        value = ttk.Label(parent, textvariable=variable, font=("Segoe UI", 10, "bold"))
        value.grid(row=row, column=1, sticky="w", pady=6)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_cpu(self):
        self.clear_content()

        title = ttk.Label(
            self.content,
            text="CPU",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(anchor="w", pady=(10, 15))

        card = ttk.Frame(
            self.content,
            padding=15,
            relief="ridge"
        )
        card.pack(fill="both", expand=True)

        self._add_row(card, "Uso", self.usage_var, 0)
        self._add_row(card, "Temperatura", self.temperature_var, 1)
        self._add_row(card, "Frequência", self.frequency_var, 2)
        self._add_row(card, "Núcleos", self.cores_var, 3)
        self._add_row(card, "Threads", self.threads_var, 4)

    def update_cpu(self):
        info = self.monitor.get_cpu_info()

        self.usage_var.set(f"{info.usage:.1f}%")
        self.temperature_var.set(info.temperature)
        self.frequency_var.set(info.frequency)
        self.cores_var.set(str(info.cores))
        self.threads_var.set(str(info.threads))

        self.root.after(250, self.update_cpu)

    def show_ram(self):
        self.clear_content()

        title = ttk.Label(
            self.content,
            text="RAM",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(anchor="w", pady=(10, 15))

        card = ttk.Frame(
            self.content,
            padding=15,
            relief="ridge"
        )
        card.pack(fill="both", expand=True)

        self._add_row(card, "Total", self.ram_total_var, 0)
        self._add_row(card, "Utilizada", self.ram_used_var, 1)
        self._add_row(card, "Disponível", self.ram_available_var, 2)
        self._add_row(card, "Uso", self.ram_percent_var, 3)
        self._add_row(card, "Cache", self.ram_cached_var, 4)

    def update_ram(self):
        info = self.monitor.get_ram_info()

        self.ram_total_var.set(f"{info.total:.2f} GB")
        self.ram_used_var.set(f"{info.used:.2f} GB")
        self.ram_available_var.set(f"{info.available:.2f} GB")
        self.ram_percent_var.set(f"{info.percent:.1f}%")
        self.ram_cached_var.set(f"{info.cached:.2f} GB")

        self.root.after(250, self.update_ram)