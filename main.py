import tkinter as tk
from PIL import Image, ImageTk

from core.monitor import SystemMonitor
from ui.dashboard import DashboardApp


def main():
    root = tk.Tk()
    
    img = Image.open("assets/favicon.png")
    img = img.convert("RGBA")

    icon = ImageTk.PhotoImage(img)

    root.iconphoto(True, icon)

    root._icon = icon

    monitor = SystemMonitor()
    DashboardApp(root, monitor)

    root.mainloop()


if __name__ == "__main__":
    main()