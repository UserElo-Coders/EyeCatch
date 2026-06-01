from ui.components.card import Card
from ui.components.row import Row


class DiskPage:
    def __init__(self, content, data):
        self.content = content
        self.data = data

    def render(self):
        if not self.data:
            return

        card = Card(self.content)

        Row(card, "Usage", f"{self.data.usage:.1f}%")
        Row(card, "Total", f"{self.data.total:.2f} GB")
        Row(card, "Free", f"{self.data.free:.2f} GB")
        Row(card, "Read", f"{self.data.read_speed:.2f} MB/s")
        Row(card, "Write", f"{self.data.write_speed:.2f} MB/s")