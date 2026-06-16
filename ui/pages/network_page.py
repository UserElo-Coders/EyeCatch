from ui.pages.resource_page import ResourcePage
from ui.pages.resource_configs import NETWORK_CONFIG


class NetworkPage(ResourcePage):
    def __init__(self, parent, view_model):
        super().__init__(parent, view_model, NETWORK_CONFIG)