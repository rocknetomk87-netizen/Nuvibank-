class IntelligenceCore:

    @staticmethod
    def analyze(user_profile):

        profile_strength = 0

        if user_profile.get("known_devices", 0) > 0:
            profile_strength += 20

        if user_profile.get("known_locations", 0) > 0:
            profile_strength += 20

        if user_profile.get("avg_transfer", 0) > 0:
            profile_strength += 20

        return {
            "profile_strength":
                profile_strength
        }
