class BasePage:
    def __init__(self, parent, view_model):
        self.parent = parent
        self.view_model = view_model

    def render(self):
        raise NotImplementedError

    def update(self, view_model):
        self.view_model = view_model