from flask import Flask

from realtime.socket.socket_engine import (
    init_socket,
    socketio
)

from realtime.live.live_events import (
    LiveEvents
)

app = Flask(__name__)

init_socket(app)

@app.route("/")
def home():

    return "NUVIBANK REALTIME ONLINE"

if __name__ == "__main__":

    LiveEvents.transfer({

        "from": "rock",

        "to": "alex",

        "amount": 5000
    })

    socketio.run(

        app,

        host="0.0.0.0",

        port=5001
    )
