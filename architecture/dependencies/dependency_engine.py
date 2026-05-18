class DependencyEngine:

    def dependencies(self):

        return {

            "CONSCIOUSNESS_CORE": [

                "SENTINEL_CORE",

                "TEMPORAL_CORE",

                "DNA_CORE"
            ],

            "IMMUNE_SYSTEM": [

                "SENTINEL_CORE"
            ],

            "SELFHEAL_CORE": [

                "IMMUNE_SYSTEM"
            ]
        }
