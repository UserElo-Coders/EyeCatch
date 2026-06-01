from ui.components.card import Card
from ui.components.row import Row


class CPUPage:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data

    def render(self):
        if not self.data:
            return

        card = Card(self.parent)

        Row(card, "Usage", f"{self.data.usage:.1f}%")
        Row(card, "Temp", self.data.temperature)
        Row(card, "Freq", self.data.frequency)
        Row(card, "Cores", str(self.data.cores))
        Row(card, "Threads", str(self.data.threads))