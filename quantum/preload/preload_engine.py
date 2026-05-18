class PreloadEngine:

    def preload_data(

        self,

        predictions
    ):

        loaded = []

        for item in predictions:

            if item == "TRANSFER":

                loaded.append(
                    "TRANSFER_CACHE"
                )

            if item == "BALANCE_CHECK":

                loaded.append(
                    "BALANCE_CACHE"
                )

        return loaded
