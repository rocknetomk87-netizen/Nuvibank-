import json

class StateStorage:

    def save(
        self,
        filename,
        data
    ):

        with open(
            filename,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load(
        self,
        filename
    ):

        with open(
            filename,
            "r"
        ) as file:

            return json.load(file)
