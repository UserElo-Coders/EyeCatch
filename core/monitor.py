import os
import time
import psutil

from models.cpu_info import CPUInfo
from models.ram_info import RAMInfo
from models.disk_info import DiskInfo
from models.network_info import NetworkInfo
from models.process_info import ProcessInfo


class SystemMonitor:
    def __init__(self):
        psutil.cpu_percent(interval=None)

        self._disk_path = "C:\\" if os.name == "nt" else "/"

        disk = psutil.disk_io_counters()
        net = psutil.net_io_counters()

        self.last_read_bytes = disk.read_bytes if disk else 0
        self.last_write_bytes = disk.write_bytes if disk else 0

        self.last_sent_bytes = net.bytes_sent if net else 0
        self.last_recv_bytes = net.bytes_recv if net else 0

        self._process_cache = []
        self._last_process_update = 0
        self._process_warmup_done = False

    def get_cpu_info(self):
        usage = psutil.cpu_percent(interval=None)

        freq = psutil.cpu_freq()
        frequency = f"{freq.current / 1000:.2f} GHz" if freq else "N/A"

        cores = psutil.cpu_count(logical=False) or 0
        threads = psutil.cpu_count(logical=True) or 0

        return CPUInfo(
            usage=usage,
            temperature=self._get_temp(),
            frequency=frequency,
            cores=cores,
            threads=threads
        )

    def _get_temp(self):
        try:
            temps = psutil.sensors_temperatures()
        except Exception:
            return "N/A"

        for group in temps.values():
            for t in group:
                if hasattr(t, "current") and t.current is not None:
                    return f"{t.current:.1f} °C"
        return "N/A"

    def get_ram_info(self):
        m = psutil.virtual_memory()
        gb = 1024 ** 3

        cached = getattr(m, "cached", None)
        cached_gb = cached / gb if cached is not None else 0

        return RAMInfo(
            total=m.total / gb,
            used=m.used / gb,
            available=m.available / gb,
            percent=m.percent,
            cached=cached_gb
        )

    def get_disk_info(self):
        d = psutil.disk_usage(self._disk_path)
        io = psutil.disk_io_counters()

        gb = 1024 ** 3
        mb = 1024 ** 2

        if io is None:
            return DiskInfo(
                usage=d.percent,
                total=d.total / gb,
                free=d.free / gb,
                read_speed=0.0,
                write_speed=0.0
            )

        read = io.read_bytes - self.last_read_bytes
        write = io.write_bytes - self.last_write_bytes

        self.last_read_bytes = io.read_bytes
        self.last_write_bytes = io.write_bytes

        seconds = 1.0

        return DiskInfo(
            usage=d.percent,
            total=d.total / gb,
            free=d.free / gb,
            read_speed=(read / seconds) / mb,
            write_speed=(write / seconds) / mb
        )

    def get_network_info(self):
        n = psutil.net_io_counters()

        sent = n.bytes_sent - self.last_sent_bytes
        recv = n.bytes_recv - self.last_recv_bytes

        self.last_sent_bytes = n.bytes_sent
        self.last_recv_bytes = n.bytes_recv

        seconds = 1.0
        kb = 1024

        return NetworkInfo(
            sent_speed=(sent / seconds) / kb,
            received_speed=(recv / seconds) / kb,
            total_sent=n.bytes_sent,
            total_received=n.bytes_recv
        )

    def get_processes(self, limit=15):
        now = time.time()

        if now - self._last_process_update < 10 and self._process_cache:
            return self._process_cache

        if not self._process_warmup_done:
            for p in psutil.process_iter():
                try:
                    p.cpu_percent(None)
                except Exception:
                    pass
            self._process_warmup_done = True
            self._last_process_update = now
            return self._process_cache

        processes = []

        for p in psutil.process_iter(["pid", "name", "status", "memory_percent"]):
            try:
                processes.append(
                    ProcessInfo(
                        pid=p.pid,
                        name=p.info.get("name") or "Unknown",
                        cpu=p.cpu_percent(interval=None),
                        memory=p.info.get("memory_percent") or 0.0,
                        status=p.info.get("status") or "unknown",
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        processes.sort(key=lambda x: (x.cpu, x.memory), reverse=True)

        self._process_cache = processes[:limit]
        self._last_process_update = now

        return self._process_cache