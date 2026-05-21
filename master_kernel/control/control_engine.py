class ControlEngine:

    def manage(self, report):

        controls = []

        for item in report:

            controls.append({

                "system": item["system"],

                "action": "MAINTAIN",

                "status": "CONTROLLED"
            })

        return controls
