import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    _global_binding_done = False
    _instances = set()

    def __init__(self, parent, *, bg="#0F1115", width=None, height=None):
        super().__init__(parent)

        self.canvas = tk.Canvas(
            self,
            bg=bg,
            highlightthickness=0,
            width=width,
            height=height
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.inner = tk.Frame(self.canvas, bg=bg)

        self.inner_id = self.canvas.create_window(
            (0, 0),
            window=self.inner,
            anchor="nw"
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind("<Destroy>", self._on_destroy, add="+")

        ScrollableFrame._instances.add(self)

        if not ScrollableFrame._global_binding_done:
            root = self.winfo_toplevel()
            root.bind_all("<MouseWheel>", ScrollableFrame._on_global_mousewheel, add="+")
            root.bind_all("<Button-4>", ScrollableFrame._on_global_mousewheel, add="+")
            root.bind_all("<Button-5>", ScrollableFrame._on_global_mousewheel, add="+")
            ScrollableFrame._global_binding_done = True

    def _on_inner_configure(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.inner_id, width=event.width)

    def _on_destroy(self, _event=None):
        ScrollableFrame._instances.discard(self)

    def _is_descendant(self, widget):
        current = widget
        while current is not None:
            if current == self.canvas or current == self.inner:
                return True
            current = getattr(current, "master", None)
        return False

    def _scroll(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
            return "break"
        if event.num == 5:
            self.canvas.yview_scroll(1, "units")
            return "break"

        delta = int(-1 * (event.delta / 120))
        if delta != 0:
            self.canvas.yview_scroll(delta, "units")
            return "break"

        return None

    @classmethod
    def _on_global_mousewheel(cls, event):
        for instance in list(cls._instances):
            if instance._is_descendant(event.widget):
                result = instance._scroll(event)
                if result == "break":
                    return "break"
        return None