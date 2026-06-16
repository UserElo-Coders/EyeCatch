import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ui.theme.tokens import SURFACE, BORDER, TEXT_PRIMARY


class ChartCard(tk.Frame):
    def __init__(self, parent, title: str, line_color="#4F8CFF"):
        super().__init__(
            parent,
            bg=SURFACE,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        self.line_color = line_color

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        tk.Label(
            self,
            text=title,
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        self.figure = Figure(figsize=(4, 2), dpi=100)
        self.figure.patch.set_facecolor(SURFACE)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(SURFACE)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        widget = self.canvas.get_tk_widget()
        widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def update_chart(self, values, ymin=None, ymax=None):
        self.ax.clear()
        self.ax.set_facecolor(SURFACE)

        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.ax.tick_params(
            left=False,
            bottom=False,
            labelleft=False,
            labelbottom=False
        )

        values = list(values or [])
        if values:
            self.ax.plot(values, color=self.line_color, linewidth=2.5)
            self.ax.set_xlim(0, max(len(values) - 1, 1))

            if ymin is None:
                ymin = min(values)
            if ymax is None:
                ymax = max(values)

            if ymin == ymax:
                delta = 1 if ymin == 0 else abs(ymin) * 0.1
                ymin -= delta
                ymax += delta

            self.ax.set_ylim(ymin, ymax)

        self.ax.grid(alpha=0.12)
        self.canvas.draw_idle()