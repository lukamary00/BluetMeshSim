from .feature import Feature


class Friend(Feature):
    def receive(self, frame):
        """
        Cashe messages.
        """
