from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
import os.path
from simulation.tiles import Surface, Slot
from .widgets import FileChooser, DeviceConfigWindow, RoomConfigWindow
from .widgets.conf_popup import ConfPopup
from simulation.network import Network

Builder.load_file("simulation/gui/main_window.kv")


class MainWindow(BoxLayout):
    map_area = ObjectProperty()
    config_panel = ObjectProperty()
    open_room = ObjectProperty()
    open_device = ObjectProperty()
    frame_canvas = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device_config = DeviceConfigWindow(self)
        self.room_config = RoomConfigWindow(self)

    def run(self, map_):
        """
        Starts simulation with new map.
        """
        surface = Surface(map_)
        self.map_area.clear_widgets()
        self.map_area.cols = surface.width
        self.open_room.disabled = False
        self.network = Network(surface, self.frame_canvas)
        for line in surface._surface:
            for tile in line:
                if isinstance(tile, Slot):
                    tile.bind(on_press=self._open_device_config)
                self.map_area.add_widget(tile)
                tile.network = self.network

    def upload_map(self):
        FileChooser(callback=self.run)

    def _open_device_config(self, slot=None):
        """
        Opens device config window for slot.

        :param slot: slot pressed by user.
        """
        self.room_config.close()
        self.device_config.open(slot)

    def _open_room_config(self):
        """
        Opens room configuration.
        """
        self.device_config.close()
        self.room_config.open()
