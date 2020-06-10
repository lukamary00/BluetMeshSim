from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from functools import partial
from simulation.nodes.elements import Element
from kivy.factory import Factory
from simulation.tabs.widgets.conf_popup import ConfPopup
from simulation.tiles import Slot


class DeviceConfigWindow(ScrollView):

    def __init__(self, main_window: 'MainWindow', **kwargs):
        super().__init__(**kwargs)
        self._config_panel = main_window.config_panel
        self._device_config_opener = main_window.open_device
        self.current_slot = None

    def new_element(self, device: dict = None):
        """
        Adds an empty device row
        :param device: dict with current device description
        """
        self.container.add_widget(DeviceRow(self, device))

    def _parse_slot(self):
        """
        Parse self.current_slot with devices and fill scroll view with them.
        """
        for device in self.current_slot.content:
            self.new_element(device)
        self.new_element()

    def open(self, slot: Slot = None):
        """
        Opens config window for slot.

        :param slot: slot with node for this config
        """
        if self.current_slot:
            self.save_previous_slot()

        if slot:
            self.current_slot = slot

        self._config_panel.clear_widgets()
        self.container.clear_widgets()
        self._parse_slot()
        self._config_panel.add_widget(self)
        self._device_config_opener.disabled = self.current_slot is None

    def close(self):
        self.save_previous_slot()

    def save_previous_slot(self):
        """
        Save last opened slot
        """
        if self.current_slot:
            self.current_slot.content = [
                device_row.chosen_device for device_row in self.container.children
                if device_row.chosen_device['device'] != '']


class DeviceRow(BoxLayout):
    open_conf = ObjectProperty()

    def __init__(self, conf_window, device: dict, **kwargs):
        super().__init__(**kwargs)
        self.conf_window = conf_window
        self.chosen_device = (
            device or {'device': '', 'publishing': '', 'subcribed': []})
        self.devices.text = self.chosen_device['device']
        self.devices.values = Element.registered_elements.keys()

    def remove(self):
        if len(self.parent.children) > 1:
            self.parent.remove_widget(self)

    def on_spinner_select(self, text):
        self.chosen_device['device'] = text

    def open_config(self):
        if self.devices.text != "":
            ConfPopup(self.conf_window, self)

    def save_config(self, config_record: dict):
        """
        Saves configuration for current device
        :param config_record: dict, that describes configuration for current device
        {
            'device': device name,
            'publishing': publishing id,
            'subcribed': subscribed topics,
        }
        """
        self.chosen_device = config_record
