"""Class describes surface on which frames are modving."""
from typing import List
from functools import partial
from simulation.network import TileType, Tile, Slot, Wall
from operator import attrgetter


class Surface:
    """
    Contain graph of tiles.

    Surface creates graph of tiles from provided map and marks there entry points.

        Purposes:
            Each frequency will contain a surface.
            Packets sent by this frequency will run across this surface.
            In case of colisions, there will be an error on the surface that
            will inform the network about it.
    """

    def __init__(self, map: List[List[int]], meters_in_tile: int = 1):
        self.entry_points, self._surface = self.from_map(map)
        self._meters_in_tile = meters_in_tile

    def wrap_surface(self, surface: List[List[int]]) -> None:
        """
        Wrap surface,by placing wall tiles on bounds.

        Because lists are passed as reference, doesn't return anything
        """
        cols = len(surface[0])
        rows = len(surface)
        surface.insert(0, [Wall()] * cols)
        surface.append([Wall()] * cols)

        def wrap_row(row):
            row.insert(0, Wall())
            row.append(Wall())

        return list(map(wrap_row, surface))

    def from_map(self, surface: List[List[int]]) -> List[Tile]:
        """Generate graph and assign entry points from provided map.

        :param surface: - array from which map will be genereated
        :param row_width: - number of elements in map row
        :return: - list of tiles, where nodes could be placed
        """
        def map_row(element, entry_points):
            """Perform row mapping to tile and save entry points."""
            tile = Tile.from_int(element)
            if isinstance(tile, Slot):
                entry_points.append(tile)
            return tile

        entry_points = []
        surface = [list(map(partial(map_row, entry_points=entry_points), row))
                   for row in surface]
        self.wrap_surface(surface)

        surface = self.assign_neingbors_and_flatten(surface)
        return entry_points, surface

    def assign_neingbors_and_flatten(self, surface: List[List[Tile]]) -> List[Tile]:
        """Bind each tile with it's left, right, upper and lower neinghbor."""

        for i, row in enumerate(surface[1:-1], start=1):
            for j, tile in enumerate(row[1:-1], start=1):
                up = surface[i-1][j]
                bottom = surface[i+1][j]
                left = surface[i][j-1]
                right = surface[i][j+1]
                tile.neinghbors = [up, bottom, left, right]
        return surface

    def calculate_distance(self, from_tile: Tile, to_tile: Tile) -> int:
        """Calculates distance in meters between two tiles."""
        return self._meters_in_tile * len(self._dijkstra(from_tile, to_tile))

    def _dijkstra(self, from_tile: Tile, to_tile: Tile) -> List[int]:
        def to_path(from_tile: Tile) -> List[Tile]:
            """Create list from shortes path in Graph."""
            path = [from_tile]
            if from_tile.previous:
                path.extend(to_path(from_tile.previous))
            return path

        def clean(surface):

            for tile in surface:
                tile.distance = float('inf')

        # unvisited = [tile for tile in self.surface if tile is not from_tile]
        flatten_surf = [item for sublist in self._surface for item in sublist]
        unvisited = []
        for tile in flatten_surf:
            if not isinstance(tile, Wall):
                tile.distance = float('inf')
                unvisited.append(tile)
        from_tile.distance = 0
        from_tile.previous = []
        current = None
        while unvisited and current is not to_tile:
            current = unvisited.pop(
                unvisited.index(min(unvisited, key=attrgetter('distance'))))
            for neinghbor in current.neinghbors:
                if neinghbor in unvisited:
                    alternetive_distance = current.distance + 1
                    if alternetive_distance < neinghbor.distance:
                        neinghbor.distance = alternetive_distance
                        neinghbor.previous = current

        clean(flatten_surf)
        return to_path(to_tile)
