import tkinter as tk
from tkinter import ttk

from ui.pages.cpu_page import CPUPage
from ui.pages.ram_page import RAMPage
from ui.pages.disk_page import DiskPage
from ui.pages.network_page import NetworkPage
from ui.pages.process_page import ProcessPage


class DashboardApp:
    def __init__(self, root: tk.Tk, monitor):
        self.root = root
        self.monitor = monitor

        self.root.title("UserEx Monitor")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        self.state = {
            "cpu": None,
            "ram": None,
            "disk": None,
            "network": None,
        }

        self.current_page_name = None
        self.current_page = None

        self._build_layout()
        self._build_sidebar()

        self.update_state()
        self.show_cpu()
        self.start_loop()

    def _build_layout(self):
        self.main = ttk.Frame(self.root)
        self.main.pack(fill="both", expand=True)

        self.sidebar = ttk.Frame(self.main, width=220)
        self.sidebar.pack(side="left", fill="y")

        self.content = ttk.Frame(self.main)
        self.content.pack(side="right", fill="both", expand=True)

    def _build_sidebar(self):
        title = ttk.Label(self.sidebar, text="UserEx Monitor", font=("Segoe UI", 14, "bold"))
        title.pack(padx=12, pady=(12, 20), anchor="w")

        ttk.Button(self.sidebar, text="CPU", command=self.show_cpu).pack(fill="x", padx=12, pady=4)
        ttk.Button(self.sidebar, text="RAM", command=self.show_ram).pack(fill="x", padx=12, pady=4)
        ttk.Button(self.sidebar, text="DISK", command=self.show_disk).pack(fill="x", padx=12, pady=4)
        ttk.Button(self.sidebar, text="NETWORK", command=self.show_network).pack(fill="x", padx=12, pady=4)
        ttk.Button(self.sidebar, text="PROCESSOS", command=self.show_process).pack(fill="x", padx=12, pady=4)

    def update_state(self):
        try:
            self.state["cpu"] = self.monitor.get_cpu_info()
        except Exception:
            self.state["cpu"] = None

        try:
            self.state["ram"] = self.monitor.get_ram_info()
        except Exception:
            self.state["ram"] = None

        try:
            self.state["disk"] = self.monitor.get_disk_info()
        except Exception:
            self.state["disk"] = None

        try:
            self.state["network"] = self.monitor.get_network_info()
        except Exception:
            self.state["network"] = None

    def start_loop(self):
        self.update_state()
        self.refresh_current_page()
        self.root.after(1000, self.start_loop)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def refresh_current_page(self):
        if self.current_page is None or self.current_page_name is None:
            return

        if self.current_page_name == "process":
            self.current_page.refresh()
        else:
            self.current_page.refresh(self.state.get(self.current_page_name))

    def show_cpu(self):
        self.current_page_name = "cpu"
        self.clear_content()
        self.current_page = CPUPage(self.content)
        self.current_page.render(self.state["cpu"])

    def show_ram(self):
        self.current_page_name = "ram"
        self.clear_content()
        self.current_page = RAMPage(self.content)
        self.current_page.render(self.state["ram"])

    def show_disk(self):
        self.current_page_name = "disk"
        self.clear_content()
        self.current_page = DiskPage(self.content)
        self.current_page.render(self.state["disk"])

    def show_network(self):
        self.current_page_name = "network"
        self.clear_content()
        self.current_page = NetworkPage(self.content)
        self.current_page.render(self.state["network"])

    def show_process(self):
        self.current_page_name = "process"
        self.clear_content()
        self.current_page = ProcessPage(self.content, self.monitor)
        self.current_page.render()