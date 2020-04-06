from simulation.network import Network, Frame
from simulation.nodes import Node
from simulation.nodes.elements import TemperatureTracker, Element
from simulation.environment import Environment
from typing import List, Tuple


class Simulation:
    """Class responsible for managing of simulation objects."""

    def __init__(self, surface):
        self._network = surface
        self._environment = Environment()

    def init_slot(self, slot_id: int, elements: List[Tuple[str, int]]):
        """
        Create all elements and register them as Node in network.

        :param slot_id: slot where element wil be placed
        :param elements: tuple of form (element_name, amount) of elements,
        that will be assigned to this node
        """
        elements = [Element.from_name(element, self._environment)
                    for element, amount in elements for i in range(amount)]
        node = Node(elements)
        self._network.register_node(node, slot_id)


def run(surface):
    sim = Simulation(surface)
    elements = [('temperaturetracker', 2)]
    sim.init_slot(1, elements)
    sim.init_slot(2, elements)

    print("Surface looks like")
    for row in sim._surface._surface:
        print(row)

    frame = Frame(source_id=1, dest_id=2)
    sim._network.transmit(frame, 900)


if __name__ == '__main__':
    surface = [
        [2, 2, 2, 1, 0, 1],
        [2, 0, 0, 0, 0, 2],
        [2, 0, 2, 0, 0, 2],
        [2, 0, 2, 2, 0, 2],
        [2, 0, 0, 0, 0, 2],
        [2, 1, 2, 2, 2, 2]
    ]
    run(surface)
