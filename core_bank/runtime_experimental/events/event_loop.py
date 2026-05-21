class EventLoop:
    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)

    def consume(self):
        if self.events:
            return self.events.pop(0)

        return None
