"""Class describes surface on which frames are modving."""
from typing import List
from functools import partial
from simulation.tiles import Tile, Slot, Wall
from operator import attrgetter


class Surface:
    """
    Create map from file.
    """

    def __init__(self, map_: List[List[int]], meters_in_tile: int = 10):
        """
        :param meters_in_tile: length of one of dimensions of square tile in meters 
        """
        self._meters_in_tile = meters_in_tile
        self._surface = self.from_map(map_)

    @property
    def width(self):
        return len(self._surface[0])

    @property
    def height(self):
        return len(self._surface)

    def from_map(self, surface: List[List[int]]) -> List[Tile]:
        """Generate graph and assign entry points from provided map.

        :param surface: - array from which map will be genereated
        :return: - list of tiles, where nodes could be placed
        """
        tiled_surface = []
        for y in range(len(surface)):
            row = []
            for x in range(len(surface[0])):
                tile = Tile.from_int(surface[y][x])
                tile.world_pos =  (x * self._meters_in_tile, y * self._meters_in_tile)
                row.append(tile)
            tiled_surface.append(row)
        return tiled_surface
