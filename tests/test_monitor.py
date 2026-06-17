from core.monitor import SystemMonitor
from core.history import HistoryManager

from unittest.mock import patch

from core.monitor import SystemMonitor




def test_network_info():
    monitor = SystemMonitor()

    network = monitor.get_network_info()

    assert network.total_sent >= 0
    assert network.total_received >= 0
    assert network.sent_speed >= 0
    assert network.received_speed >= 0

def test_process_cache():
    monitor = SystemMonitor()

    first = monitor.get_processes()
    second = monitor.get_processes()

    assert isinstance(first, list)
    assert isinstance(second, list)

def test_invalid_history_key():
    history = HistoryManager()

    assert history.get("banana") == []

def test_cpu_temperature():
    monitor = SystemMonitor()

    temp = monitor._get_temp()

    assert isinstance(temp, str)


def test_cpu_info():
    monitor = SystemMonitor()

    cpu = monitor.get_cpu_info()

    assert cpu is not None
    assert 0 <= cpu.usage <= 100

def test_ram_info():
    monitor = SystemMonitor()

    ram = monitor.get_ram_info()

    assert ram.total > 0
    assert ram.used >= 0

def test_disk_info():
    monitor = SystemMonitor()

    disk = monitor.get_disk_info()

    assert disk.total > 0