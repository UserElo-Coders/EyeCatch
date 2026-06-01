import psutil
import time

from models.cpu_info import CPUInfo
from models.ram_info import RAMInfo
from models.disk_info import DiskInfo
from models.network_info import NetworkInfo
from models.process_info import ProcessInfo


class SystemMonitor:
    def __init__(self):
        psutil.cpu_percent(interval=None)

        disk = psutil.disk_io_counters()
        net = psutil.net_io_counters()

        self.last_read_bytes = disk.read_bytes
        self.last_write_bytes = disk.write_bytes

        self.last_sent_bytes = net.bytes_sent
        self.last_recv_bytes = net.bytes_recv

        self._process_cache = []
        self._last_process_update = 0

    # ---------------- CPU ----------------
    def get_cpu_info(self):
        usage = psutil.cpu_percent(interval=None)

        freq = psutil.cpu_freq()
        frequency = f"{freq.current/1000:.2f} GHz" if freq else "N/A"

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
        except:
            return "N/A"

        for group in temps.values():
            for t in group:
                if hasattr(t, "current"):
                    return f"{t.current:.1f} ºC"
        return "N/A"

    # ---------------- RAM ----------------
    def get_ram_info(self):
        m = psutil.virtual_memory()

        gb = 1024 ** 3

        return RAMInfo(
            total=m.total / gb,
            used=m.used / gb,
            available=m.available / gb,
            percent=m.percent,
            cached=getattr(m, "cached", 0) / gb if getattr(m, "cached", None) else 0
        )

    # ---------------- DISK ----------------
    def get_disk_info(self):
        d = psutil.disk_usage("/")

        io = psutil.disk_io_counters()

        gb = 1024 ** 3
        mb = 1024 ** 2

        read = io.read_bytes - self.last_read_bytes
        write = io.write_bytes - self.last_write_bytes

        self.last_read_bytes = io.read_bytes
        self.last_write_bytes = io.write_bytes

        return DiskInfo(
            usage=d.percent,
            total=d.total / gb,
            free=d.free / gb,
            read_speed=(read / 0.25) / mb,
            write_speed=(write / 0.25) / mb
        )

    # ---------------- NETWORK ----------------
    def get_network_info(self):
        n = psutil.net_io_counters()

        sent = n.bytes_sent - self.last_sent_bytes
        recv = n.bytes_recv - self.last_recv_bytes

        self.last_sent_bytes = n.bytes_sent
        self.last_recv_bytes = n.bytes_recv

        kb = 1024

        return NetworkInfo(
            sent_speed=(sent / 0.25) / kb,
            received_speed=(recv / 0.25) / kb,
            total_sent=n.bytes_sent,
            total_received=n.bytes_recv
        )

    # ---------------- PROCESS (CACHE) ----------------
    def get_processes(self, limit=25):
        now = time.time()

        if now - self._last_process_update < 2:
            return self._process_cache

        processes = []

        for p in psutil.process_iter(["pid", "name", "status"]):
            try:
                processes.append(
                    ProcessInfo(
                        pid=p.pid,
                        name=p.info["name"] or "Unknown",
                        cpu=p.cpu_percent(interval=None),
                        memory=p.memory_percent(),
                        status=p.info["status"]
                    )
                )
            except:
                continue

        processes.sort(key=lambda x: (x.cpu, x.memory), reverse=True)

        self._process_cache = processes[:limit]
        self._last_process_update = now

        return self._process_cache