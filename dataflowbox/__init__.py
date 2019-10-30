import threading
from datetime import datetime


class DataFlowBox:

    def __init__(self):
        self.sources = []
        self.lock = threading.Lock()

    def add_source(self, source):
        source.set_lock(self.lock)
        self.sources.append(source)

    def start(self):
        for source in self.sources:
            source.start()

        for source in self.sources:
            source.join()


