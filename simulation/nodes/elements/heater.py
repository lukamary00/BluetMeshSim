from .element import Element
from simulation.network import Content, Frame
from simulation.environment import Environment
from enum import IntEnum


class State(IntEnum):
    HEATING = 1
    WAITING = 2


class Heater(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = State.WAITING

    def on_receive(self, frame: Frame) -> None:
        if frame.content is Content.START_HEAT and self.state is State.WAITING:
            self.state = State.HEATING
            Environment.heaters.append(self)
            self.node.slot.background_color = (1, .5, .5, .5)

        elif frame.content is Content.STOP_HEAT and self.state is State.HEATING:
            self.state = State.WAITING
            Environment.heaters.remove(self)
            self.node.slot.background_color = (.5, 1, .5, .5)

    def on_remove(self):
        super().on_remove()
        if self in Environment.heaters:
            Environment.heaters.remove(self)
