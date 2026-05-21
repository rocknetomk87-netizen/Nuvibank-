class StreamEngine:
    def process(self, event):
        return {
            "streamed": True,
            "event": event
        }
