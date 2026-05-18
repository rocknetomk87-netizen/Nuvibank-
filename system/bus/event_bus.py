class EventBus:

    listeners = {}

    @classmethod
    def subscribe(
        cls,
        event_name,
        callback
    ):

        if event_name not in cls.listeners:

            cls.listeners[event_name] = []

        cls.listeners[event_name].append(
            callback
        )

    @classmethod
    def emit(
        cls,
        event_name,
        data
    ):

        if event_name in cls.listeners:

            for callback in cls.listeners[event_name]:

                callback(data)
