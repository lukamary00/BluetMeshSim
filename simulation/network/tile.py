"""Contains description of `Tile` from which  `Surface` consists."""
from abc import ABC, abstractmethod
from typing import List, TypeVar, Dict
from enum import Enum, auto
from simulation.network import Frame
from simulation.nodes import Node
# Means that content could be frame or node
Content = TypeVar('Content', Frame, Node)


class TileType(Enum):
    """Type of created tile."""
    EMPTY = 0
    SLOT = 1
    WALL = 2


class TileState(Enum):
    """State of tile."""
    EMPTY = auto()
    NOT_EMPTY = auto()


class Tile(ABC):
    """Describes the most basic empty element  of `Surface`."""
    tile_types = {}
    tiles_created = 0
    # TODO Move assigment to Network
    frames_passed = 0

    def __init__(self):
        """
        On create all tiles are empty because they still hadn't received.
        nothing, and there no devices connected to them.
        """
        Tile.tiles_created += 1
        self.id = Tile.tiles_created
        self.last_received_frame_id = -1
        self._content: Content = None
        self.neinghbors = []

    def assign_frame_id(self, frame: Frame) -> int:
        """
        Assigns frame id, to frame so it could be identified on `Tile` level
        :param frame: - unregistered Frame
        :return: - assigned id
        """
        Tile.frames_passed += 1
        frame.frame_id = Tile.frames_passed
        return Tile.frames_passed

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, frame: Frame):
        if frame.frame_id is None:
            self.assign_frame_id(frame)
        self.last_received_frame_id = frame.frame_id
        self._content = frame

    @staticmethod
    def from_int(tile_as_int: int, **kwargs):
        """
        Creates new Tile from int if int is a valid type.
        :param `tile_as_int` - integer representation of tile.
        :return: - newly created corresponding to this integer
        """
        if tile_as_int not in Tile.tile_types.keys():
            raise ValueError(f"{tile_as_int} not a valid tile type")
        return Tile.tile_types[tile_as_int](**kwargs)

    def propagate(self) -> None:
        """
        Propagate frame content on surface.
        :param `trace` - tiles, already visited by this frame
        """
        for tile in self.neinghbors:
            if self.content.frame_id != tile.last_received_frame_id:
                tile.receive(self.content)
        self._state = TileState.EMPTY

    def __init_subclass__(cls):
        Tile.tile_types[TileType[str.upper(cls.__name__)].value] = cls

    @abstractmethod
    def receive(self, val: Frame, from_tile) -> None:
        """Decribe what should happend with Frame after tile will receive it"""
        raise NotImplementedError

    def __repr__(self):
        return str.lower(self.__class__.__name__)


class Slot(Tile):
    """
    Type of `Tile` to which device can be assigned.
    """

    def __init__(self):
        super().__init__()
        self.content = None

    def assign_node(self, node: Node):
        """
        Assign new node to this slot.

        :param node: new node to assign
        """
        self.content = node

    def receive(self, frame: Frame, path_loss: float) -> None:
        """
        Check if frame could be received with given path_loss.

        :param frame: received frame
        :param path_loss: calculated path_loss
        """
        self.content.receive(frame)
        print(f"Received {frame}")


class Wall(Tile):
    """
    Type of Tile from which Frame can't pass
    """

    def receive(self, val: Frame):
        pass


class Empty(Tile):
    """
    Type of tile where nothing can't happend.
    """

    def receive(self, val):
        self.content = val
        self.propagate()
