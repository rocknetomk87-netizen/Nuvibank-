from datetime import datetime

class LogEngine:

    logs = []

    @classmethod
    def log(

        cls,

        event,

        data
    ):

        cls.logs.append({

            "event": event,

            "data": data,

            "timestamp": str(datetime.now())
        })

    @classmethod
    def get_logs(cls):

        return cls.logs
