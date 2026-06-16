import tkinter as tk

from ui.theme import setup_theme
from ui.components.sidebar import Sidebar

from ui.pages import (
    DashboardPage,
    CPUPage,
    RAMPage,
    DiskPage,
    NetworkPage,
    ProcessPage,
)


class DashboardApp:
    def __init__(self, root, monitor, history):
        self.root = root
        self.monitor = monitor
        self.history = history

        setup_theme(self.root)

        self.root.title("EyeCatch")
        self.root.geometry("1280x720")

        self.state = {
            "cpu": None,
            "ram": None,
            "disk": None,
            "network": None,
            "processes": [],
        }

        self.current_page_name = "dashboard"
        self.current_page = None

        self._build_ui()

        self.pages = {
            "dashboard": DashboardPage,
            "cpu": CPUPage,
            "ram": RAMPage,
            "disk": DiskPage,
            "network": NetworkPage,
            "process": ProcessPage,
        }

        self._update_state()
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

    def _update_state(self):
        self.state["cpu"] = self.monitor.get_cpu_info()
        self.state["ram"] = self.monitor.get_ram_info()
        self.state["disk"] = self.monitor.get_disk_info()
        self.state["network"] = self.monitor.get_network_info()

        self.history.update(
            cpu_usage=self.state["cpu"].usage,
            ram_percent=self.state["ram"].percent,
            disk_usage=self.state["disk"].usage,
            network_speed=self.state["network"].sent_speed + self.state["network"].received_speed,
        )

        if self.current_page_name == "process":
            self.state["processes"] = self.monitor.get_processes(limit=15)

    def _build_view_model(self):
        return {
            **self.state,
            "history": self.history,
            "health": self._calculate_health(),
        }

    def _calculate_health(self):
        cpu = self.state["cpu"].usage if self.state["cpu"] else 0
        ram = self.state["ram"].percent if self.state["ram"] else 0
        disk = self.state["disk"].usage if self.state["disk"] else 0

        score = 100
        score -= cpu * 0.20
        score -= ram * 0.20
        score -= disk * 0.10

        return max(0, int(score))

    def _loop(self):
        self._update_state()

        if self.current_page:
            self.current_page.update(self._build_view_model())

        self.root.after(1000, self._loop)

    def navigate(self, page):
        self.current_page_name = page

        if hasattr(self, "sidebar"):
            self.sidebar.set_active(page)

        for widget in self.content.winfo_children():
            widget.destroy()

        if page == "process" and not self.state.get("processes"):
            self.state["processes"] = self.monitor.get_processes(limit=15)

        page_class = self.pages[page]
        self.current_page = page_class(self.content, self._build_view_model())
        self.current_page.render()