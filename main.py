import os
import sys
import tkinter as tk
from PIL import Image, ImageTk

from core.monitor import SystemMonitor
from core.history import HistoryManager
from ui.dashboard import DashboardApp


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    root = tk.Tk()

    icon_path = resource_path("assets/favicon.png")
    if os.path.exists(icon_path):
        img = Image.open(icon_path).convert("RGBA")
        icon = ImageTk.PhotoImage(img)
        root.iconphoto(True, icon)
        root._icon = icon

    monitor = SystemMonitor()
    history = HistoryManager(maxlen=60)

    DashboardApp(root, monitor, history)
    root.mainloop()


if __name__ == "__main__":
    main()