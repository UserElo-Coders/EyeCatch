import tkinter as tk

from ui.theme import setup_theme
from ui.components.sidebar import Sidebar

from ui.pages.cpu_page import CPUPage
from ui.pages.ram_page import RAMPage
from ui.pages.disk_page import DiskPage
from ui.pages.network_page import NetworkPage
from ui.pages.process_page import ProcessPage


class DashboardApp:
    def __init__(self, root, monitor):
        self.root = root
        self.monitor = monitor

        setup_theme(self.root)

        self.root.geometry("1000x600")
        self.root.title("EyeCatch")

        self.state = {}

        self.current_page = None
        self.current_page_name = "cpu"

        self._build_ui()
        self._loop()

        self.pages = {
            "cpu": CPUPage,
            "ram": RAMPage,
            "disk": DiskPage,
            "network": NetworkPage,
            "process": ProcessPage
        }

        self.navigate("cpu")

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
        self.state = {
            "cpu": self.monitor.get_cpu_info(),
            "ram": self.monitor.get_ram_info(),
            "disk": self.monitor.get_disk_info(),
            "network": self.monitor.get_network_info(),
            "process": self.monitor.get_processes()
        }

        if self.current_page:
            self.navigate(self.current_page_name)

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