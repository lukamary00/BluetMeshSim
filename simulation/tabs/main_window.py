from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import os.path
from simulation.utils import FileManager
from simulation.network import Surface


class MainWindow(Screen):
    map_area = ObjectProperty()

    def __init__(self, screen_manager, **kwargs):
        kv_path = f"simulation/gui/{str.lower(self.__class__.__name__)}.kv"
        Builder.load_file(kv_path)
        super(MainWindow, self).__init__(**kwargs)
        self.sm = screen_manager

    def run(self, filename):
        """Simple demo, that prints file converted to tilemap into console."""
        # Replace with normal selection and validation
        int_surface = FileManager.parse(filename[0])
        obj_surf = Surface(int_surface)
        text = ""
        for line in obj_surf._surface:
            text += "".join([str(elem) + "  " for elem in line])
            text += "\n"
        self.map_area.text = text
