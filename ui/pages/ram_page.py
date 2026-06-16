from ui.pages.resource_page import ResourcePage
from ui.pages.resource_configs import RAM_CONFIG


class RAMPage(ResourcePage):
    def __init__(self, parent, view_model):
        super().__init__(parent, view_model, RAM_CONFIG)