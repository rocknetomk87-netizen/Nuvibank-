class PatternMemory:

    def detect(

        self,

        events
    ):

        patterns = []

        if events.count(
            "FAILED_LOGIN"
        ) > 3:

            patterns.append(
                "BRUTE_FORCE_PATTERN"
            )

        return patterns
