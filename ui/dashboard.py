import tkinter as tk

from ui.theme import setup_theme
from ui.components.sidebar import Sidebar

from ui.pages.cpu_page import CPUPage
from ui.pages.ram_page import RAMPage
from ui.pages.disk_page import DiskPage
from ui.pages.network_page import NetworkPage
from ui.pages.process_page import ProcessPage

from core.history import HistoryManager


class DashboardApp:
    def __init__(self, root, monitor):
        self.root = root
        self.monitor = monitor

        setup_theme(self.root)

        self.root.geometry("1000x600")
        self.root.title("EyeCatch")

        self.history = HistoryManager()

        self.state = {}

        self.current_page = None
        self.current_page_name = "dasboard"

        self._build_ui()

        self.pages = {
            "cpu": CPUPage,
            "ram": RAMPage,
            "disk": DiskPage,
            "network": NetworkPage,
            "process": ProcessPage
        }

        self.state["cpu"] = self.monitor.get_cpu_info()
        self.state["ram"] = self.monitor.get_ram_info()
        self.state["disk"] = self.monitor.get_disk_info()
        self.state["network"] = self.monitor.get_network_info()

        self.navigate("dashboard")
        self._loop()

    def _build_ui(self):
        self.container = tk.Frame(self.root, bg="#0F1115")
        self.container.pack(fill="both", expand=True)

        self.sidebar = Sidebar(self.container, self.navigate)
        self.sidebar.pack(side="left", fill="y")

        self.main = tk.Frame(self.container, bg="#0F1115")
        self.main.pack(side="right", fill="both", expand=True)

        self.content = tk.Frame(self.main, bg="#0F1115")
        self.content.pack(fill="both", expand=True)

    def _loop(self):
        self.state["cpu"] = self.monitor.get_cpu_info()
        self.state["ram"] = self.monitor.get_ram_info()
        self.state["disk"] = self.monitor.get_disk_info()
        self.state["network"] = self.monitor.get_network_info()

        self.history.update(
            self.state["cpu"].usage,
            self.state["ram"].percent,
            self.state["disk"].usage,
            self.state["network"].received_speed
        )

        if self.current_page_name == "process":
            self.state["process"] = self.monitor.get_processes()

        if self.current_page:
            self.current_page.update(
                self.state.get(self.current_page_name)
            )

        self.root.after(1000, self._loop)

    def navigate(self, page):
        self.current_page_name = page

        for w in self.content.winfo_children():
            w.destroy()

        self.current_page = self.pages[page](
            self.content,
            self.state.get(page)
        )

        self.current_page.render()