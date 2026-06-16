from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass(frozen=True)
class MetricSpec:
    title: str
    attr: str
    formatter: Callable[[Any], str]


@dataclass(frozen=True)
class ChartSpec:
    title: str
    history_key: str
    color: str
    xlabel: str
    ylabel: str
    ymin: Optional[float] = None
    ymax: Optional[float] = None


@dataclass(frozen=True)
class ResourcePageConfig:
    title: str
    subtitle: str
    resource_key: str
    metrics: list[MetricSpec]
    charts: list[ChartSpec]


CPU_CONFIG = ResourcePageConfig(
    title="CPU Overview",
    subtitle="Real-time CPU monitoring",
    resource_key="cpu",
    metrics=[
        MetricSpec("Usage", "usage", lambda v: f"{v:.1f}%"),
        MetricSpec("Temperature", "temperature", lambda v: v),
        MetricSpec("Frequency", "frequency", lambda v: v),
        MetricSpec("Cores", "cores", lambda v: str(v)),
        MetricSpec("Threads", "threads", lambda v: str(v)),
    ],
    charts=[
        ChartSpec("CPU History", "cpu_usage", "#4F8CFF", "Seconds", "Usage (%)", 0, 100),
    ],
)

RAM_CONFIG = ResourcePageConfig(
    title="Memory Overview",
    subtitle="Real-time RAM monitoring",
    resource_key="ram",
    metrics=[
        MetricSpec("Usage", "percent", lambda v: f"{v:.1f}%"),
        MetricSpec("Used", "used", lambda v: f"{v:.2f} GB"),
        MetricSpec("Available", "available", lambda v: f"{v:.2f} GB"),
        MetricSpec("Total", "total", lambda v: f"{v:.2f} GB"),
        MetricSpec("Cached", "cached", lambda v: f"{v:.2f} GB"),
    ],
    charts=[
        ChartSpec("RAM History", "ram_percent", "#7C5CFF", "Seconds", "Usage (%)", 0, 100),
    ],
)

DISK_CONFIG = ResourcePageConfig(
    title="Disk Overview",
    subtitle="Storage usage and I/O performance",
    resource_key="disk",
    metrics=[
        MetricSpec("Usage", "usage", lambda v: f"{v:.1f}%"),
        MetricSpec("Total", "total", lambda v: f"{v:.2f} GB"),
        MetricSpec("Free", "free", lambda v: f"{v:.2f} GB"),
        MetricSpec("Read Speed", "read_speed", lambda v: f"{v:.2f} MB/s"),
        MetricSpec("Write Speed", "write_speed", lambda v: f"{v:.2f} MB/s"),
    ],
    charts=[
        ChartSpec("Disk Usage History", "disk_usage", "#22C55E", "Seconds", "Usage (%)", 0, 100),
    ],
)

NETWORK_CONFIG = ResourcePageConfig(
    title="Network Overview",
    subtitle="Traffic usage and bandwidth monitoring",
    resource_key="network",
    metrics=[
        MetricSpec("Upload", "sent_speed", lambda v: f"{v:.2f} KB/s"),
        MetricSpec("Download", "received_speed", lambda v: f"{v:.2f} KB/s"),
        MetricSpec("Total Sent", "total_sent", lambda v: f"{v / (1024 ** 2):.2f} MB"),
        MetricSpec("Total Received", "total_received", lambda v: f"{v / (1024 ** 2):.2f} MB"),
    ],
    charts=[
        ChartSpec("Network History", "network_speed", "#F59E0B", "Seconds", "KB/s", 0, None),
    ],
)