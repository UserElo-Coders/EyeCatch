from collections import deque


class HistoryMananger:

    def __init__(self):

        self.cpu = deque(maxlen=60)
        self.ram = deque(maxlen=60)
        self.disk = deque(maxlen=60)
        self.network = deque(maxlen=60)
    
    def update(self, cpu, ram, disk, network):

        self.cpu.append(cpu)
        self.ram.append(ram)
        self.disk.append(disk)
        self.network.append(network)
        
    def get_cpu(self):
        return list(self.cpu)
    
    def get_ram(self):
        return list(self.ram)
    
    def get_disk(self):
        return list(self.disk)
    
    def get_network(self):
        return list(self.network)