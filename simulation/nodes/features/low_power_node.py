from .feature import Feature

class LowPowerNode(Feature):
    def receive(self, frame):
        """
        Does nothing.
        """