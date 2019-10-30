import time
from ..base import SourceThread


class Tail(SourceThread):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        f = open(self.filename)
        f.seek(0, 2)
        pos = f.tell()

        while True:
            line = f.readline()
            if line:
                self.emit('raw_log', line.strip())
                pos = f.tell()
            else:
                f.seek(pos)
                time.sleep(0.1)

