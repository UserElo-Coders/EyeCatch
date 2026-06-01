from dataclasses import dataclass

@dataclass
class RAMInfo:
    total: float
    used: float
    available: float
    percent: float
    cached: float