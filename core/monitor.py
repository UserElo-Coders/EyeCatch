import psutil
from models.cpu_info import CPUInfo
from models.ram_info import RAMInfo

class SystemMonitor:
    def __init__(self):
        # "Heats" the CPU reading to avoid returning 0 at the first usage
        psutil.cpu_percent(interval=None)

    def get_cpu_info(self) -> CPUInfo:
        usage = psutil.cpu_percent(interval=None)

        freq = psutil.cpu_freq()

        if freq and freq.current :
            frequency = f"{freq.current / 1000:.2f} GHz"
        else:
            frequency = "N/A"

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
    
    def _get_cpu_temperature(self) -> str :
        try:
            temps = psutil.sensors_temperatures()
        except (AttributeError, NotImplementedError):
            return "N/A"
        
        if not temps:
            return "N/A"
        
        for sensors_list in temps.values():
            for sensor in sensors_list:
                current = getattr(sensor, "current", None)
                if current is not None:
                    return f"{current:.1f} ºC"
                
        return "N/A"
    
    def get_ram_info(self) -> RAMInfo :
        memory = psutil.virtual_memory()

        gb = 1024 ** 3

        total = memory.total / gb
        used = memory.used / gb
        available = memory.available / gb
        percent = memory.percent
        
        cached = getattr(memory, "cached", None)

        if cached is not None:
            cached = cached / gb
        else:
            cached = 0.0

        return RAMInfo(
            total=total,
            used=used,
            available=available,
            percent=percent,
            cached=cached
        )