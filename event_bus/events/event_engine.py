class EventEngine:

    def create_event(self, event, payload):

        return {
            "event": event,
            "payload": payload,
            "status": "CREATED"
        }
