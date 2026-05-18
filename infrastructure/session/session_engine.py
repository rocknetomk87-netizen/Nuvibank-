import uuid

class SessionEngine:

    sessions = {}

    @classmethod
    def create_session(
        cls,
        username
    ):

        token = str(uuid.uuid4())

        cls.sessions[token] = username

        return token

    @classmethod
    def validate(
        cls,
        token
    ):

        return cls.sessions.get(token)
