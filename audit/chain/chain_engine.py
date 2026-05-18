from datetime import datetime

class ChainEngine:

    def create_event(

        self,

        event,
        previous_hash,
        current_hash
    ):

        return {

            "timestamp": (
                str(
                    datetime.utcnow()
                )
            ),

            "event": event,

            "previous_hash": (
                previous_hash
            ),

            "hash": (
                current_hash
            )
        }
