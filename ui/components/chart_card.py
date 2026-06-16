import tkinter as tk

import numpy as np
import matplotlib.patheffects as pe
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from ui.theme.tokens import SURFACE, BORDER, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY


class ChartCard(tk.Frame):
    def __init__(
        self,
        parent,
        title: str,
        line_color="#4F8CFF",
        xlabel="Seconds",
        ylabel="Value",
        show_axes: bool = False,
    ):
        super().__init__(
            parent,
            bg=SURFACE,
            highlightthickness=1,
            highlightbackground=BORDER,
        )

        self.line_color = line_color
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.show_axes = show_axes

        self._values = np.array([], dtype=float)
        self._display_values = np.array([], dtype=float)
        self._ymin = None
        self._ymax = None

        self._animation_after_id = None
        self._animation_frames = 8
        self._animation_step = 0
        self._animation_from = np.array([], dtype=float)
        self._animation_to = np.array([], dtype=float)

        self._last_hover_index = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        top = tk.Frame(self, bg=SURFACE)
        top.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=0)

        left = tk.Frame(top, bg=SURFACE)
        left.grid(row=0, column=0, sticky="w")

        tk.Label(
            left,
            text=title,
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")

        self.value_label = tk.Label(
            left,
            text="--",
            bg=SURFACE,
            fg=PRIMARY,
            font=("Segoe UI", 20, "bold"),
        )
        self.value_label.pack(anchor="w", pady=(2, 0))

        right = tk.Frame(top, bg=SURFACE)
        right.grid(row=0, column=1, sticky="e")

        self.legend_chip = tk.Frame(right, bg="#1D212B", padx=10, pady=4)
        self.legend_chip.pack(anchor="e")

        dot = tk.Canvas(
            self.legend_chip,
            width=10,
            height=10,
            bg="#1D212B",
            highlightthickness=0,
        )
        dot.create_oval(2, 2, 8, 8, fill=self.line_color, outline=self.line_color)
        dot.pack(side="left", padx=(0, 6))

        tk.Label(
            self.legend_chip,
            text="Live",
            bg="#1D212B",
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left")

        self.axes_button = tk.Button(
            right,
            text="Axes",
            command=self.toggle_axes,
            bg=SURFACE,
            fg=TEXT_SECONDARY,
            activebackground=SURFACE,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 8, "bold"),
        )
        self.axes_button.pack(anchor="e", pady=(8, 0))

        self.figure = Figure(figsize=(4.6, 2.5), dpi=100)
        self.figure.patch.set_facecolor(SURFACE)
        self.figure.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.12)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(SURFACE)

        self.glow_line, = self.ax.plot([], [], color=self.line_color, linewidth=8, alpha=0.08, zorder=2)
        self.main_line, = self.ax.plot([], [], color=self.line_color, linewidth=2.8, zorder=3)
        self.point = self.ax.scatter([], [], s=54, color=self.line_color, edgecolors="#FFFFFF", linewidths=0.6, zorder=5)

        self.tooltip = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(12, 12),
            textcoords="offset points",
            ha="left",
            va="bottom",
            color=TEXT_PRIMARY,
            fontsize=8,
            bbox=dict(
                boxstyle="round,pad=0.35",
                facecolor="#1D212B",
                edgecolor=self.line_color,
                linewidth=1,
            ),
            arrowprops=dict(
                arrowstyle="-",
                color=self.line_color,
                linewidth=1,
            ),
            zorder=6,
        )
        self.tooltip.set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        widget = self.canvas.get_tk_widget()
        widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.canvas.mpl_connect("motion_notify_event", self._on_mouse_move)
        self.canvas.mpl_connect("figure_leave_event", self._on_leave)

        self._configure_axes()

    def destroy(self):
        if self._animation_after_id is not None:
            try:
                self.after_cancel(self._animation_after_id)
            except Exception:
                pass
            self._animation_after_id = None
        super().destroy()

    def _configure_axes(self):
        for spine in self.ax.spines.values():
            spine.set_visible(False)

        if self.show_axes:
            self.ax.tick_params(
                axis="x",
                colors=TEXT_SECONDARY,
                labelsize=7,
                length=0,
                pad=4,
            )
            self.ax.tick_params(
                axis="y",
                colors=TEXT_SECONDARY,
                labelsize=7,
                length=0,
                pad=4,
            )
            self.ax.xaxis.set_major_locator(MaxNLocator(4))
            self.ax.yaxis.set_major_locator(MaxNLocator(4))
            self.ax.set_xlabel(self.xlabel, color=TEXT_SECONDARY, fontsize=8, labelpad=6)
            self.ax.set_ylabel(self.ylabel, color=TEXT_SECONDARY, fontsize=8, labelpad=6)
        else:
            self.ax.tick_params(
                axis="both",
                which="both",
                bottom=False,
                left=False,
                labelbottom=False,
                labelleft=False,
            )
            self.ax.set_xlabel("")
            self.ax.set_ylabel("")

        self.ax.grid(alpha=0.10, linestyle="--", linewidth=0.6)

    def toggle_axes(self):
        self.show_axes = not self.show_axes
        self.redraw()

    def update_chart(self, values, ymin=None, ymax=None, current_value=None):
        new_values = np.array(list(values or []), dtype=float)

        if current_value is None:
            current_value = float(new_values[-1]) if len(new_values) else 0.0

        self.value_label.config(text=self._format_value(current_value))

        self._ymin = ymin
        self._ymax = ymax

        if len(self._display_values) == 0:
            self._display_values = new_values
            self._values = new_values
            self.redraw()
            return

        if self._animation_after_id is not None:
            try:
                self.after_cancel(self._animation_after_id)
            except Exception:
                pass
            self._animation_after_id = None

        self._animation_from = self._pad_series(self._display_values, len(new_values))
        self._animation_to = self._pad_series(new_values, len(self._animation_from))
        self._animation_step = 0
        self._animate_step()

    def _animate_step(self):
        progress = self._animation_step / max(self._animation_frames - 1, 1)
        eased = self._ease_out_cubic(progress)

        interpolated = self._animation_from + (
            (self._animation_to - self._animation_from) * eased
        )

        self._display_values = interpolated
        self.redraw()

        self._animation_step += 1
        if self._animation_step < self._animation_frames and self.winfo_exists():
            self._animation_after_id = self.after(24, self._animate_step)
        else:
            self._animation_after_id = None
            self._display_values = self._animation_to
            self.redraw()

    def redraw(self):
        self._configure_axes()

        values = np.array(self._display_values, dtype=float)
        if len(values) == 0:
            self.main_line.set_data([], [])
            self.glow_line.set_data([], [])
            self.point.set_offsets(np.empty((0, 2)))
            self.tooltip.set_visible(False)
            self.canvas.draw_idle()
            return

        x = np.arange(len(values), dtype=float)

        if len(values) >= 3:
            x_smooth = np.linspace(x.min(), x.max(), max(len(values) * 18, 90))
            y_smooth = np.interp(x_smooth, x, values)
        else:
            x_smooth = x
            y_smooth = values

        ymin = self._ymin if self._ymin is not None else float(np.min(y_smooth))
        ymax = self._ymax if self._ymax is not None else float(np.max(y_smooth))

        if ymin == ymax:
            delta = 1 if ymin == 0 else abs(ymin) * 0.1
            ymin -= delta
            ymax += delta

        self.ax.set_ylim(ymin, ymax)
        self.ax.set_xlim(0, max(len(values) - 1, 1))

        self.glow_line.set_data(x_smooth, y_smooth)
        self.glow_line.set_path_effects([
            pe.Stroke(linewidth=10, foreground=self.line_color, alpha=0.10),
            pe.Normal(),
        ])

        self.main_line.set_data(x_smooth, y_smooth)
        self.main_line.set_path_effects([
            pe.Stroke(linewidth=5.2, foreground=self.line_color, alpha=0.12),
            pe.Normal(),
        ])

        last_x = x[-1]
        last_y = values[-1]

        self.point.set_offsets(np.array([[last_x, last_y]]))
        self.point.set_visible(True)

        if self.tooltip.get_visible():
            self.tooltip.xy = (last_x, last_y)
            self.tooltip.set_text(self._format_value(last_y))

        # área preenchida recriada só uma vez por frame
        for coll in list(self.ax.collections):
            if coll is not self.point:
                try:
                    coll.remove()
                except Exception:
                    pass

        self.ax.fill_between(
            x_smooth,
            y_smooth,
            ymin,
            color=self.line_color,
            alpha=0.18,
            linewidth=0,
            zorder=1,
        )

        self.figure.canvas.draw_idle()

    def _on_mouse_move(self, event):
        if event.inaxes != self.ax or len(self._display_values) == 0 or event.xdata is None:
            if self.tooltip.get_visible():
                self.tooltip.set_visible(False)
                self.canvas.draw_idle()
            return

        idx = int(np.clip(round(event.xdata), 0, len(self._display_values) - 1))
        if self._last_hover_index == idx and self.tooltip.get_visible():
            return

        self._last_hover_index = idx

        x = np.arange(len(self._display_values), dtype=float)
        y = np.array(self._display_values, dtype=float)

        px = x[idx]
        py = y[idx]

        self.tooltip.xy = (px, py)
        self.tooltip.set_text(self._format_value(py))
        self.tooltip.set_visible(True)
        self.canvas.draw_idle()

    def _on_leave(self, _event):
        self._last_hover_index = None
        if self.tooltip.get_visible():
            self.tooltip.set_visible(False)
            self.canvas.draw_idle()

    def _pad_series(self, series, target_len):
        series = np.array(series, dtype=float)
        if len(series) == target_len:
            return series
        if len(series) == 0:
            return np.zeros(target_len, dtype=float)
        if len(series) < target_len:
            pad_value = series[-1]
            pad = np.full(target_len - len(series), pad_value, dtype=float)
            return np.concatenate([series, pad])
        return series[:target_len]

    def _ease_out_cubic(self, t):
        return 1 - pow(1 - t, 3)

    def _format_value(self, value):
        try:
            value = float(value)
            if abs(value) >= 100:
                return f"{value:.0f}"
            if abs(value) >= 10:
                return f"{value:.1f}"
            return f"{value:.2f}"
        except Exception:
            return str(value)