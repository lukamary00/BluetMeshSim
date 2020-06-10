from .feature import Feature
from simulation.network import Type


class Relay(Feature):

    def on_receive(self, frame):
        """
        Transmits frame further to network,
        """
        frame.ttl = str(int(frame.ttl) - 1)
        if int(frame.ttl) > 0:
            frame.type = Type.RELAYED
            self.device.node.send(frame, relayed=True)
