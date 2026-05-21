class HistoryEngine:

    def record(self, event):

        return {
            "recorded": True,
            "event": event,
            "history": "UPDATED"
        }
