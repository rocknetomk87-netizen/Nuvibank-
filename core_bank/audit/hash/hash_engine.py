import hashlib

class HashEngine:

    def generate(

        self,

        data
    ):

        encoded = (
            str(data)
            .encode()
        )

        return hashlib.sha256(
            encoded
        ).hexdigest()
