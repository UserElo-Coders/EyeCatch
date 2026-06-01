from ui.components.card import Card
from ui.components.row import Row


class RAMPage:
    def __init__(self, content, data):
        self.content = content
        self.data = data

    def render(self):
        if not self.data:
            return

        card = Card(self.content)

        Row(card, "Total", f"{self.data.total:.2f} GB")
        Row(card, "Used", f"{self.data.used:.2f} GB")
        Row(card, "Available", f"{self.data.available:.2f} GB")
        Row(card, "Usage", f"{self.data.percent:.1f}%")
        Row(card, "Cached", f"{self.data.cached:.2f} GB")