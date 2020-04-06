"""Desribes classes used for `Node` communication."""
from simulation.network import Surface
from simulation.network import Frame
from simulation.nodes import Node
from typing import List
from itertools import permutations
from math import log10


class Network:
    """Describes medium where all communication happend."""
    """
    Table of constants for ITU indoor propagation model
    1.(freq MHz, floors): rate
    2.freq: rate
    """
    _floor_penetration_loss_factor = {
        (900, 1): 9,
        (900, 2): 19,
        (900, 3): 24,
        (2000, 1): 15,
        (2000, 2): 19,
        (2000, 3): 23
    }
    _distance_power_loss_coefficient = {
        900: 33,
        2000: 30
    }

    def __init__(self, map: List[List[int]]):
        self._surface = Surface(map)
        self._route_table = {}
        self._entry_points = {}

    def register_node(self, node: Node, slot: int):
        """
        Add node to network, so it can start share messages.

        :param `node`: - that represents this node.
        :param `slot`: - id of slot on surface, where this node will be assigned
        """
        self._entry_points[node.id] = self._surface.entry_points[slot]
        self._entry_points[node.id].assign_node(node)
        print(f"Device was succesfully registered on slot {slot}")

    def transmit(self, frame: Frame, frequency: int):
        """Send frame given as argument."""
        distance = self._calculate_distance(frame.source_id, frame.dest_id)
        path_loss = self._calculate_path_loss(frequency, distance, 1)
        print(
            f"Transmitting frame: {str(frame)} on distance {distance} meters with path loss {path_loss}")
        self._entry_points[frame.dest_id].receive(frame, path_loss)

    def _calculate_distance(self, from_node: 'device id', to_node: 'device id'):
        """
        Calculates distance between two nodes, based on data in _device_entry_points.
        """
        route = (self._entry_points[from_node], self._entry_points[to_node])
        distance = [self._route_table.setdefault(
            route_perm, None) for route_perm in permutations(route)]
        if not any(distance):
            distance = [self._surface.calculate_distance(*route)]
            self._route_table[route] = distance[0]
        return list(map(lambda el: el, distance))[0]

    def _calculate_path_loss(self, f: int, d: int, n: int) -> float:
        """
        Calculate path loss based on ITU indoor propagation model.

        :param f: frequency
        :param d: distance between between transmiter and reciver
        :param n: number of floors between transmiter and reciver
        :returns path_loss: path_loss coefficient for given params
        """
        return 20 * log10(f) + self._distance_power_loss_coefficient[(f)]\
            * log10(d) + self._floor_penetration_loss_factor[(f, n)] - 28
