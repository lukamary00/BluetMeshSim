from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from os import curdir

class ScreenFileChooser(Screen):
    """Provides interface for interaction with filesystem."""

    file_chooser = ObjectProperty()

    def __init__(self, screen_manager, simulation_runner, **kwargs):
        kv_path = f"simulation/gui/widgets/{str.lower(self.__class__.__name__)}.kv"
        Builder.load_file(kv_path)
        super(ScreenFileChooser, self).__init__(**kwargs)
        self.file_chooser.filters = [lambda folder,
                                     filename: not filename.endswith('.sys')]
        self.file_chooser.path = curdir
        self.sm = screen_manager
        self.sim_runner = simulation_runner

    def upload_map(self, filename):
        # TODO replace with kivy event
        self.sim_runner.run(filename)
        self.close()

    def close(self):
        self.sm.transition.duration = 1
        self.sm.transition = FadeTransition()
        self.sm.current = 'main'
