from ui.components.card import Card
from ui.components.row import Row


class NetworkPage:
    def __init__(self, content, data):
        self.content = content
        self.data = data

    def render(self):
        if not self.data:
            return

        card = Card(self.content)

        Row(card, "Sent", f"{self.data.sent_speed:.2f} KB/s")
        Row(card, "Recv", f"{self.data.received_speed:.2f} KB/s")
        Row(card, "Total Sent", f"{self.data.total_sent / (1024**2):.2f} MB")
        Row(card, "Total Recv", f"{self.data.total_received / (1024**2):.2f} MB")