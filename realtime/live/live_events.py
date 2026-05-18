from realtime.socket.socket_engine import (
    socketio
)

class LiveEvents:

    @staticmethod
    def transfer(data):

        socketio.emit(

            "transfer",

            data
        )

    @staticmethod
    def fraud_alert(data):

        socketio.emit(

            "fraud_alert",

            data
        )

    @staticmethod
    def notification(data):

        socketio.emit(

            "notification",

            data
        )
