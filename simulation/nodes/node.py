"""Contains abstract base for all nodes"""
from simulation.network import Frame
# https://www.bluetooth.com/blog/3-key-factors-that-determinethe-range-of-bluetooth/
from .elements import Element


class Node:
    """Device/collection of devices, that could communicate via network."""
    count = 0

    def __init__(self, content: list, slot, feature=None):
        """
        :param content: list of dicts that describes what devices should be contained in this node.
        {
            'device': self.device,
            'publishing': self.publishing,
            'subcribed': self.subcribed,
            'role'
        }
        """
        self.slot = slot
        self.id = self._set_id()
        self._elements = [Element.registered_elements[element['device']](
            content=element, node=self) for element in content]
        self._transmitting_power = 17
        self._sensitivity = 5
        """
        Minimum power of signal, that this node could receive
        """

    @property
    def pos(self):
        return self.slot.pos

    @property
    def transmitting_power(self) -> int:
        return self._transmitting_power

    @transmitting_power.setter
    def transmitting_power(self, value):
        self._transmitting_power = value

    @property
    def sensitivity(self) -> int:
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value) -> int:
        self._sensitivity = value

    def _set_id(self) -> int:
        Node.count += 1
        return Node.count

    def receive(self, frame: Frame):
        """Receives frame passed to device."""
        for element in self._elements:
            element.receive(frame)

    def could_receive(self, signal_power) -> bool:
        return self.sensitivity < signal_power

    def add_element(self, device):
        # Change
        dev = Element.from_name(device['device'])
        self._elements.append(dev)

    def send(self, frame, relayed=False):
        if frame.topic != '' or relayed:
            self.slot.network.broadcast(frame, src=self)

    def on_remove(self):
        for element in self._elements:
            element.on_remove()
