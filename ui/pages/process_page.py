from ui.pages.base_page import BasePage
from ui.components.page_header import PageHeader
from ui.components.process_table import ProcessTable


class ProcessPage(BasePage):
    def __init__(self, parent, view_model):
        super().__init__(parent, view_model)
        self.table = None

    def render(self):
        PageHeader(
            self.parent,
            "Processes",
            "Top running processes by CPU and memory usage"
        )

        self.table = ProcessTable(self.parent)
        self.table.render()
        self.update(self.view_model)

    def update(self, view_model):
        super().update(view_model)

        processes = view_model.get("processes", []) or []
        if self.table is not None:
            self.table.update(processes)