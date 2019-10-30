from ..base import Pipe


class HttpRequestRate(Pipe):
    """Count HTTP requests per second.
    """
    def __init__(self):
        super().__init__()
        self.count = 0

    def notify(self, logevent):
        if logevent.event_type == 'parsed_log':
            self.count += 1
        elif logevent.event_type == 'timer':
            self.emit('http_request_rate', { 'datetime': logevent.payload, 'count': self.count })
            self.count = 0

