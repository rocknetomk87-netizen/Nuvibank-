from flask_socketio import SocketIO

socketio = SocketIO(

    cors_allowed_origins="*"
)

def init_socket(app):

    socketio.init_app(app)

    return socketio
