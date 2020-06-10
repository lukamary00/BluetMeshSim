from os.path import join, curdir
from os import listdir


class FileManager:
    map_dir = join(curdir, "simulation/maps")

    """Provides common operations on files"""
    @staticmethod
    def load_map(map_name):
        """Read from filename and parse it as int 2d array."""
        with open(join(FileManager.map_dir, map_name), 'r') as file:
            parsed_surface = [list(map(int, line[:-1])) for line in file]
        return parsed_surface

    @staticmethod
    def get_maps_filenames():
        return listdir(FileManager.map_dir)
