import uuid
from flask import g


def generate_request_id():

    g.request_id = str(uuid.uuid4())
