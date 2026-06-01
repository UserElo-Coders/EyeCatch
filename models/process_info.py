from dataclasses import dataclass

@dataclass
class ProcessInfo:
    pid: int
    name: str
    cpu: float
    memory: float
    status: str