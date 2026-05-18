class DiscoveryEngine:

    def __init__(self):

        self.services = {}

    def register(

        self,

        name,
        host
    ):

        self.services[name] = host

    def discover(

        self,

        name
    ):

        return self.services.get(name)
