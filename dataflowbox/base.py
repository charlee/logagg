import threading

class Target:
    def notify(self, event):
        raise NotImplemented()


class Source: 
    def __init__(self):
        super().__init__()
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def emit(self, event_type, payload):
        for subscriber in self.subscribers:
            subscriber.notify(Event(event_type, payload))


class SourceThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.source = Source(*args, **kwargs)

    def set_lock(self, lock):
        self.lock = lock

    def subscribe(self, subscriber):
        self.source.subscribe(subscriber)

    def emit(self, event_type, payload):
        if self.lock:
            self.lock.acquire()
            self.source.emit(event_type, payload)
            self.lock.release()
        else:
            raise ValueError('Lock not configured')

    def run(self):
        raise NotImplemented()



class Pipe(Source, Target):
    pass


class Event:
    def __init__(self, event_type, payload):
        self.event_type = event_type
        self.payload = payload
