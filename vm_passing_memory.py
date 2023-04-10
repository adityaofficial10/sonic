from multiprocessing.managers import BaseManager

class DataObject:
    def __init__(self, data):
        self.data = data

class SharedMemory:
    def __init__(self):
        self.value = {}

    def store(self, data):
        self.value = data
    
    def read(self):
        return self.value

class SharedMemoryManager(BaseManager):
    pass

SharedMemoryManager.register("SharedMemory", SharedMemory)