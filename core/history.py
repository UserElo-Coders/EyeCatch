from collections import deque


class HistoryManager:
    """
    Stores historical values used by dashboard charts.

    Limits stored samples to prevent memory growth.
    """

    def __init__(self, maxlen: int = 60):
        self.cpu_usage = deque(maxlen=maxlen)
        self.ram_percent = deque(maxlen=maxlen)
        self.disk_usage = deque(maxlen=maxlen)
        self.network_speed = deque(maxlen=maxlen)

    def update(
        self,
        cpu_usage: float,
        ram_percent: float,
        disk_usage: float,
        network_speed: float
    ) -> None:
        self.cpu_usage.append(cpu_usage)
        self.ram_percent.append(ram_percent)
        self.disk_usage.append(disk_usage)
        self.network_speed.append(network_speed)

    def get(self, name: str) -> list[float]:
        series = getattr(self, name, None)

        if series is None:
            return []

        return list(series)