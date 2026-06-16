from core.monitor import SystemMonitor


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