from ui.components.card import Card
from ui.components.process_table import ProcessTable


class ProcessPage:
    def __init__(self, content, data):
        self.content = content
        self.data = data

    def render(self):
        if not self.data:
            return

        card = Card(self.content)

        ProcessTable(card, self.data)