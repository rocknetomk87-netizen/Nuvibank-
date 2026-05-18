import hashlib


def generate_device_fingerprint(user_agent, ip):

    raw = f"{user_agent}:{ip}"

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()
