from . import Element
from kivy.clock import Clock
from simulation.environment import Environment
from simulation.network import Content

class Termometr(Element):
    def __init__(self, content, node):
        # TODO Make configurable
        super().__init__(content, node, use_scheduler=True)
        self._lower_threshold = 29
        self._upper_threshold = 31

    def do_action(self, dt):
        if Environment.temperature < self._lower_threshold:
            self.send(Content.START_HEAT)
        elif Environment.temperature > self._upper_threshold:
            self.send(Content.STOP_HEAT)
