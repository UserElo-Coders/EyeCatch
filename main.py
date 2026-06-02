import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

from core.monitor import SystemMonitor
from ui.dashboard import DashboardApp


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    root = tk.Tk()
    root.title("EyeCatch")
    root.geometry("900x500")
    root.resizable(False, False)

    icon_path = resource_path("assets/favicon.png")

    img = Image.open(icon_path).convert("RGBA")
    icon = ImageTk.PhotoImage(img)

    root.iconphoto(True, icon)

    root._icon = icon

    monitor = SystemMonitor()

    DashboardApp(root, monitor)

    root.mainloop()


if __name__ == "__main__":
    main()