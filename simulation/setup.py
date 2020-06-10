from simulation.network import Network, Frame
from simulation.nodes import Node
from simulation.nodes.elements import Element
from simulation.environment import Environment
from typing import List, Tuple

"""
CLI for simulation.
"""


class Simulation:
    """Class responsible for managing of simulation objects."""

    def __init__(self, surface):
        self._network = Network(surface)
        self._environment = Environment()

    def init_slot(self, slot_id: int, elements: List[Tuple[str, int]]):
        """
        Create all elements and register them as Node in network.

        :param slot_id: slot where element wil be placed
        :param elements: tuple of form (element_name, amount) of elements,
        that will be assigned to this node
        """
        # elements = [Element.from_name(element, self._environment)
        #             for element, amount in elements for i in range(amount)]
        # node = Node(elements)
        # self._network.register_node(node, slot_id)


def run(surface):
    pass
    # sim = Simulation(surface)
    # elements = [('termometr', 2)]
    # sim.init_slot(1, elements)
    # sim.init_slot(2, elements)

    # print("Surface looks like")
    # for row in sim._network._surface._surface:
    #     print(row)

    # frame = Frame(source_id=1, dest_id=2)
    # sim._network.transmit(frame, 900)


