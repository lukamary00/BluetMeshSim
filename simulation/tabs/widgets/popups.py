from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from simulation.utils import FileManager


class FileChooser(Popup):
    """
    Implements a popup window for map selection.
    """
    map_spinner = ObjectProperty()

    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.map_spinner.values = FileManager.get_maps_filenames()
        self.map_spinner.text = FileManager.get_maps_filenames()[0]
        self.user_callback = callback
        self.open()

    def upload_file(self) -> None:
        parsed_map = FileManager.load_map(self.map_spinner.text)
        self.user_callback(parsed_map)
        self.dismiss()


