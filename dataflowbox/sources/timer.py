import time
import pytz
from datetime import datetime
from ..base import SourceThread


class Timer(SourceThread):
    def __init__(self, tzname, accuracy='second'):
        super().__init__()
        self.accuracy = accuracy

        self.tz = pytz.timezone(tzname)


    def get_now(self):
        now = datetime.now(self.tz).replace(microsecond=0)
        if self.accuracy == 'minute':
            now = now.replace(second=0)

        return now


    def run(self):
        last_time = self.get_now()
        while True:
            current_time = self.get_now()
            if current_time != last_time:
                self.emit('timer', last_time)
                last_time = current_time
            time.sleep(0.1)

