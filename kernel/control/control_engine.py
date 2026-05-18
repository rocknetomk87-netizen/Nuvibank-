class ControlEngine:

    def optimize(

        self,

        cpu
    ):

        if cpu > 80:

            return {

                "cache": "BOOST",

                "workers": "SCALE_UP",

                "routing": "ADAPTIVE"
            }

        return {

            "status": "STABLE"
        }
