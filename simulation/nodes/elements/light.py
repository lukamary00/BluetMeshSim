from . import Element
from simulation.network import Content, Frame
from simulation.environment import Environment
from enum import IntEnum


class State(IntEnum):
    ON = 1
    OFF = 0


class Light(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = State.OFF
        self.node.slot.background_color = (.65, 0.1, 0.1, .5)

    def on_receive(self, frame: Frame) -> None:
        if frame.content is Content.LIGHT_ON and self.state is State.OFF:
            self.state = State.ON
            self.node.slot.background_color = (1, 1, .5, .5)

        elif frame.content is Content.LIGHT_OFF and self.state is State.ON:
            self.state = State.OFF
            self.node.slot.background_color = (.65, 0.1, 0.1, .5)

        elif self.state is State.OFF:
            self.node.slot.background_color = (.65, 0.1, 0.1, .5)

