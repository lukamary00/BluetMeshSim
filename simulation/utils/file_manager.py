class FileManager:
    """Provides common operations on files"""
    @staticmethod
    def parse(filename):
        """Read from filename and parse it as int 2d array."""
        with open(filename, 'r') as file:
            parsed_surface = [
                map(int, line[:-1]) for line in file]
        return parsed_surface
