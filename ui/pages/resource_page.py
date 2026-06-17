import tkinter as tk

from ui.pages.base_page import BasePage
from ui.components.page_header import PageHeader
from ui.components.metric_card import MetricCard
from ui.components.chart_card import ChartCard
from ui.components.scrollable_frame import ScrollableFrame
from ui.pages.resource_configs import ResourcePageConfig

from ui.theme import tokens


class ResourcePage(BasePage):
    def __init__(self, parent, view_model, config: ResourcePageConfig):
        super().__init__(parent, view_model)
        self.config = config
        self.metric_vars = {}
        self.metric_cards = []
        self.chart_cards = []

    def render(self):
        self.metric_vars.clear()
        self.metric_cards.clear()
        self.chart_cards.clear()

        scroll = ScrollableFrame(self.parent, bg=tokens.BACKGROUND)
        scroll.pack(fill="both", expand=True)

        root = scroll.inner

        PageHeader(root, self.config.title, self.config.subtitle)

        metrics_frame = tk.Frame(root, bg=tokens.BACKGROUND)
        metrics_frame.pack(fill="x", padx=12, pady=(0, 10))

        metrics_frame.columnconfigure(0, weight=1, uniform="cards")
        metrics_frame.columnconfigure(1, weight=1, uniform="cards")

        metrics_count = len(self.config.metrics)
        metrics_rows = (metrics_count + 1) // 2
        for row in range(metrics_rows):
            metrics_frame.rowconfigure(row, weight=1)

        for idx, metric in enumerate(self.config.metrics):
            row = idx // 2
            col = idx % 2
            span = 2 if (metrics_count % 2 == 1 and idx == metrics_count - 1) else 1

            var = tk.StringVar(value="--")
            self.metric_vars[metric.attr] = var

            card = MetricCard(metrics_frame, metric.title, var)
            card.grid(row=row, column=col, columnspan=span, padx=12, pady=12, sticky="nsew")
            self.metric_cards.append(card)

        charts_frame = tk.Frame(root, bg=tokens.BACKGROUND)
        charts_frame.pack(fill="both", expand=True, padx=12, pady=(0, 24))

        charts_frame.columnconfigure(0, weight=1, uniform="charts")
        charts_frame.columnconfigure(1, weight=1, uniform="charts")

        chart_count = len(self.config.charts)
        chart_rows = (chart_count + 1) // 2
        for row in range(chart_rows):
            charts_frame.rowconfigure(row, weight=1)

        for i, chart in enumerate(self.config.charts):
            row = i // 2
            col = i % 2
            span = 2 if (chart_count % 2 == 1 and i == chart_count - 1) else 1

            chart_card = ChartCard(
                charts_frame,
                chart.title,
                chart.color,
                chart.xlabel,
                chart.ylabel
            )
            chart_card.grid(row=row, column=col, columnspan=span, padx=12, pady=12, sticky="nsew")
            self.chart_cards.append((chart, chart_card))

        self.update(self.view_model)

    def update(self, view_model):
        super().update(view_model)

        resource = view_model.get(self.config.resource_key)
        history = view_model.get("history")

        if resource is None:
            return

        for metric in self.config.metrics:
            raw_value = getattr(resource, metric.attr, None)
            self.metric_vars[metric.attr].set(metric.formatter(raw_value))

        if history is not None:
            for chart_spec, chart_card in self.chart_cards:
                series = history.get(chart_spec.history_key) or []
                current_value = series[-1] if series else 0
                chart_card.update_chart(
                    series,
                    chart_spec.ymin,
                    chart_spec.ymax,
                    current_value=current_value
                )