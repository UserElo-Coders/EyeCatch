import tkinter as tk

from ui.pages.base_page import BasePage
from ui.components.page_header import PageHeader
from ui.components.metric_card import MetricCard
from ui.components.chart_card import ChartCard
from ui.components.scrollable_frame import ScrollableFrame

from ui.theme import tokens


class DashboardPage(BasePage):
    def __init__(self, parent, view_model):
        super().__init__(parent, view_model)
        self.vars = {}
        self.chart_widgets = {}

    def render(self):
        scroll = ScrollableFrame(self.parent, bg=tokens.BACKGROUND)
        scroll.pack(fill="both", expand=True)
        root = scroll.inner

        PageHeader(
            root,
            "Dashboard",
            "Overview of CPU, RAM, Disk and Network activity"
        )

        top = tk.Frame(root, bg=tokens.BACKGROUND)
        top.pack(fill="x", padx=12, pady=(0, 10))

        for i in range(4):
            top.columnconfigure(i, weight=1, uniform="top_cards")
        top.rowconfigure(0, weight=1)

        self.vars["cpu"] = tk.StringVar(value="--")
        self.vars["ram"] = tk.StringVar(value="--")
        self.vars["disk"] = tk.StringVar(value="--")
        self.vars["network"] = tk.StringVar(value="--")

        MetricCard(top, "CPU Usage", self.vars["cpu"]).grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        MetricCard(top, "RAM Usage", self.vars["ram"]).grid(row=0, column=1, padx=12, pady=12, sticky="nsew")
        MetricCard(top, "Disk Usage", self.vars["disk"]).grid(row=0, column=2, padx=12, pady=12, sticky="nsew")
        MetricCard(top, "Network", self.vars["network"]).grid(row=0, column=3, padx=12, pady=12, sticky="nsew")

        charts = tk.Frame(root, bg=tokens.BACKGROUND)
        charts.pack(fill="both", expand=True, padx=12, pady=(0, 24))

        charts.columnconfigure(0, weight=1, uniform="charts")
        charts.columnconfigure(1, weight=1, uniform="charts")
        charts.rowconfigure(0, weight=1)
        charts.rowconfigure(1, weight=1)

        self.chart_widgets["cpu"] = ChartCard(charts, "CPU History", "#4F8CFF", "Seconds", "Usage (%)")
        self.chart_widgets["ram"] = ChartCard(charts, "RAM History", "#7C5CFF", "Seconds", "Usage (%)")
        self.chart_widgets["disk"] = ChartCard(charts, "Disk History", "#22C55E", "Seconds", "Usage (%)")
        self.chart_widgets["network"] = ChartCard(charts, "Network History", "#F59E0B", "Seconds", "KB/s")

        self.chart_widgets["cpu"].grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        self.chart_widgets["ram"].grid(row=0, column=1, padx=12, pady=12, sticky="nsew")
        self.chart_widgets["disk"].grid(row=1, column=0, padx=12, pady=12, sticky="nsew")
        self.chart_widgets["network"].grid(row=1, column=1, padx=12, pady=12, sticky="nsew")

        self.update(self.view_model)

    def update(self, view_model):
        super().update(view_model)

        cpu = view_model.get("cpu")
        ram = view_model.get("ram")
        disk = view_model.get("disk")
        network = view_model.get("network")
        history = view_model.get("history")

        if cpu:
            self.vars["cpu"].set(f"{cpu.usage:.1f}%")
        if ram:
            self.vars["ram"].set(f"{ram.percent:.1f}%")
        if disk:
            self.vars["disk"].set(f"{disk.usage:.1f}%")
        if network:
            self.vars["network"].set(f"{network.sent_speed + network.received_speed:.2f} KB/s")

        if history is not None:
            cpu_series = history.get("cpu_usage") or []
            ram_series = history.get("ram_percent") or []
            disk_series = history.get("disk_usage") or []
            network_series = history.get("network_speed") or []

            self.chart_widgets["cpu"].update_chart(cpu_series, 0, 100, cpu_series[-1] if cpu_series else 0)
            self.chart_widgets["ram"].update_chart(ram_series, 0, 100, ram_series[-1] if ram_series else 0)
            self.chart_widgets["disk"].update_chart(disk_series, 0, 100, disk_series[-1] if disk_series else 0)
            self.chart_widgets["network"].update_chart(
                network_series,
                0,
                None,
                network_series[-1] if network_series else 0
            )