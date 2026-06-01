import psutil
import time
import threading

from models.cpu_info import CPUInfo
from models.ram_info import RAMInfo
from models.disk_info import DiskInfo
from models.network_info import NetworkInfo
from models.process_info import ProcessInfo


class SystemMonitor:
    def __init__(self):
        psutil.cpu_percent(interval=None)

        disk_io = psutil.disk_io_counters()
        self.last_read_bytes = disk_io.read_bytes
        self.last_write_bytes = disk_io.write_bytes

        net = psutil.net_io_counters()
        self.last_sent_bytes = net.bytes_sent
        self.last_received_bytes = net.bytes_recv

        self._process_cache = []
        self._process_lock = threading.Lock()

        self._running = True

        self._start_process_worker()

    def get_cpu_info(self) -> CPUInfo:
        usage = psutil.cpu_percent(interval=None)

        freq = psutil.cpu_freq()
        frequency = f"{freq.current / 1000:.2f} GHz" if freq else "N/A"

        temperature = self._get_cpu_temperature()

        cores = psutil.cpu_count(logical=False) or 0
        threads = psutil.cpu_count(logical=True) or 0

        return CPUInfo(
            usage=usage,
            temperature=temperature,
            frequency=frequency,
            cores=cores,
            threads=threads
        )

    def _get_cpu_temperature(self) -> str:
        try:
            temps = psutil.sensors_temperatures()
        except (AttributeError, NotImplementedError):
            return "N/A"

        if not temps:
            return "N/A"

        for sensors in temps.values():
            for sensor in sensors:
                if hasattr(sensor, "current"):
                    return f"{sensor.current:.1f} ºC"

        return "N/A"

    def get_ram_info(self) -> RAMInfo:
        mem = psutil.virtual_memory()
        gb = 1024 ** 3

        cached = getattr(mem, "cached", 0.0) or 0.0

        return RAMInfo(
            total=mem.total / gb,
            used=mem.used / gb,
            available=mem.available / gb,
            percent=mem.percent,
            cached=cached / gb
        )

    def get_disk_info(self) -> DiskInfo:
        disk = psutil.disk_usage("/")
        io = psutil.disk_io_counters()

        gb = 1024 ** 3
        mb = 1024 ** 2
        seconds = 1.0

        read_delta = io.read_bytes - self.last_read_bytes
        write_delta = io.write_bytes - self.last_write_bytes

        self.last_read_bytes = io.read_bytes
        self.last_write_bytes = io.write_bytes

        return DiskInfo(
            usage=disk.percent,
            total=disk.total / gb,
            free=disk.free / gb,
            read_speed=(read_delta / seconds) / mb,
            write_speed=(write_delta / seconds) / mb
        )

    def get_network_info(self) -> NetworkInfo:
        net = psutil.net_io_counters()

        kb = 1024
        seconds = 1.0

        sent_delta = net.bytes_sent - self.last_sent_bytes
        recv_delta = net.bytes_recv - self.last_received_bytes

        self.last_sent_bytes = net.bytes_sent
        self.last_received_bytes = net.bytes_recv

        return NetworkInfo(
            sent_speed=(sent_delta / seconds) / kb,
            received_speed=(recv_delta / seconds) / kb,
            total_sent=net.bytes_sent,
            total_received=net.bytes_recv
        )

    def _start_process_worker(self):
        def worker():
            for p in psutil.process_iter():
                try:
                    p.cpu_percent(None)
                except:
                    pass

            while self._running:
                processes = []

                for proc in psutil.process_iter(["pid", "name", "status"]):
                    try:
                        cpu = proc.cpu_percent(None)
                        memory = proc.memory_percent()

                        processes.append(
                            ProcessInfo(
                                pid=proc.pid,
                                name=proc.info.get("name") or "Unknown",
                                cpu=cpu,
                                memory=memory,
                                status=proc.info.get("status") or "unknown"
                            )
                        )

                    except (psutil.NoSuchProcess,
                            psutil.AccessDenied,
                            psutil.ZombieProcess):
                        continue

                processes.sort(key=lambda p: (p.cpu, p.memory), reverse=True)

                with self._process_lock:
                    self._process_cache = processes[:30]

                time.sleep(1)

        threading.Thread(target=worker, daemon=True).start()

    def get_processes(self, limit: int = 30):
        with self._process_lock:
            return self._process_cache[:limit]

    def stop(self):
        self._running = False