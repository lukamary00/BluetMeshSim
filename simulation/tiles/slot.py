from kivy.uix.button import Button
from kivy.properties import ListProperty
from simulation.nodes import Node
from .tile import Tile


class Slot(Tile, Button):
    """
    Type of `Tile` to which device can be assigned.
    """
    background_color = ListProperty()

    def __init__(self):
        self._content = []
        super().__init__()
        self._node = None
        """
        Node placed in this slot.
        """
        self._network = None

    @property
    def node(self):
        return self._node

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, value):
        self._network = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content: dict):
        """
        :param new_content: add new device to current slot
        {
            'device': self.device,
            'publishing': self.publishing,
            'subcribed': self.subcribed,
        }
        """
        if self._node is None:
            self._network.add_slot(self)
        else:
            self._node.on_remove()
        self._content = new_content
        self._node = Node(new_content, self)
        self.background_color = (.5, 1, .5, .5)


    def __str__(self):
        return str(self.content)
