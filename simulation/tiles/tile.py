"""Contains description of `Tile` from which  `Surface` consists."""
from enum import Enum
from typing import Tuple
from simulation.network import Frame
from kivy.uix.label import Label


class TileType(Enum):
    """Type of created tile. Used for map parsing."""
    EMPTY = 0
    SLOT = 1
    WALL = 2


class Tile:
    """
    Element of Surface.
    """
    tile_types = {}
    def __init__(self):
        super().__init__()
        self._pos = None

    @property
    def world_pos(self) -> Tuple[int, int]:
        """
        Position of tile in the world.
        """
        return self._pos

    @world_pos.setter
    def world_pos(self, value: Tuple[int, int]):
        self._pos = value

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

    def __init_subclass__(cls):
        Tile.tile_types[TileType[str.upper(cls.__name__)].value] = cls

    def __str__(self):
        return str.lower(self.__class__.__name__)


class Wall(Tile, Label):
    """
    Tile through which Frame can't pass
    """
    def __init__(self):
        super().__init__()


class Empty(Tile, Label):
    """
    Tile where nothing can't happend.
    """
    def __init__(self):
        super().__init__()
