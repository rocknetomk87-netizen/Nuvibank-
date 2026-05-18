class LoadBalancer:

    @staticmethod
    def distribute(load):

        if load > 1000:

            return "HIGH_LOAD"

        if load > 500:

            return "MEDIUM_LOAD"

        return "NORMAL_LOAD"
