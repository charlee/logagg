from ..base import Target


class Print(Target):
    def notify(self, event):
        print(event.event_type, event.payload)

