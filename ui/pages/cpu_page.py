from ui.pages.resource_page import ResourcePage
from ui.pages.resource_configs import CPU_CONFIG


class CPUPage(ResourcePage):
    def __init__(self, parent, view_model):
        super().__init__(parent, view_model, CPU_CONFIG)