"""Desribes classes used for `Node` communication."""
from simulation.tiles import Surface
from simulation.network import Frame
from simulation.nodes import Node
from typing import List, Tuple
from math import log10, sqrt


class Network:
    """
    Implement logic of frame transmission.
    """

    def __init__(self, surface: Surface, frame_canvas):
        self._surface = surface
        self._existing_slots = []
        self._freqeuncy = 2400
        """
        Standart Bluetooth frequency
        """
        self._floor_loss_factor = 15
        """
        Constant from ITU indoor propagation model
        """
        self._distance_loss_factor = 30
        """
        Constant from ITU indoor propagation model
        """
        self.frame_canvas = frame_canvas

    def add_slot(self, new_slot):
        """
        Add new node to the network.

        :param new_node: node to be added.
        """
        self._existing_slots.append(new_slot)

    def broadcast(self, frame: Frame, src: Node):
        """
        Broadcast frame to the network.

        :param frame: frame to be broadcasted
        :param src: node that sending this frame
        """
        for slot in self._existing_slots:
            if slot.node is src or not slot.node:
                continue
            distance = self._calculate_distance(
                src.slot.world_pos, slot.world_pos)
            path_loss = self._calculate_path_loss(self._freqeuncy, distance)
            if slot.node.could_receive(src.transmitting_power - path_loss/10):
                frame.instantiate(self.frame_canvas, src.pos, slot.node)

    def _calculate_path_loss(self, f: int, d: int) -> float:
        """
        Calculate path loss based on ITU indoor propagation model.

        :param f: frequency
        :param d: distance between between transmiter and reciver
        :returns path_loss: path loss in dB
        """
        return 20 * log10(f) + self._distance_loss_factor * log10(d) + self._floor_loss_factor - 28

    def _calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calculates euclidian distance between two points.
        """
        return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1])**2)
