class ProfileEngine:

    @staticmethod
    def build(events):

        total = 0

        transfers = 0

        locations = set()

        devices = set()

        for event in events:

            if event["type"] == "TRANSFER":

                total += event["amount"]

                transfers += 1

            locations.add(
                event.get("location", "UNKNOWN")
            )

            devices.add(
                event.get("device", "UNKNOWN")
            )

        avg = 0

        if transfers > 0:

            avg = total / transfers

        return {

            "avg_transfer": avg,

            "known_locations": len(locations),

            "known_devices": len(devices)
        }
