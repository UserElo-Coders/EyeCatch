from ui.pages.resource_page import ResourcePage
from ui.pages.resource_configs import DISK_CONFIG


class DiskPage(ResourcePage):
    def __init__(self, parent, view_model):
        super().__init__(parent, view_model, DISK_CONFIG)