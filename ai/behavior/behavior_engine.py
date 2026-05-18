from datetime import datetime


class BehaviorProfile:

    def __init__(self):

        self.login_hours = []
        self.transfer_patterns = []
        self.devices = []
        self.locations = []

    def register_login(self, hour):

        self.login_hours.append(hour)

    def register_transfer(self, amount):

        self.transfer_patterns.append(amount)

    def register_device(self, device):

        if device not in self.devices:
            self.devices.append(device)

    def register_location(self, location):

        if location not in self.locations:
            self.locations.append(location)

    def analyze_behavior(self):

        return {
            "known_devices": len(self.devices),
            "known_locations": len(self.locations),
            "avg_transfer": (
                sum(self.transfer_patterns)
                / len(self.transfer_patterns)
            ) if self.transfer_patterns else 0
        }
