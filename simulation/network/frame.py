"""Decribe messages that are passing through network."""
from enum import IntEnum, Enum
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.properties import StringProperty


class Content(IntEnum):
    START_HEAT = 0
    STOP_HEAT = 1
    LIGHT_ON = 2
    LIGHT_OFF = 3


class Type(Enum):
    MSG = 'white'
    RELAYED = 'yellow'
    FRIEND_REQUEST = 'green'


class Frame:
    """
    Describe frame, that devices send to each other.
    """

    def __init__(self, topic, ttl, content=None, type=Type.MSG):
        """
        :param topic: topic of this message
        :param ttl: how many hops this frame can made
        """
        self.topic = topic
        self.ttl = ttl
        self.content = content
        self.type = Type.MSG

    def instantiate(self, layout, pos, dest):
        """Adds widget representing this frame to provided layout"""
        FrameContainer(layout, pos, dest, self)

    def __str__(self):
        return f"Frame on topic '{self.topic}'. TTL: {self.ttl} with content: {self.content.name}"


class FrameContainer(Widget):
    color = StringProperty()

    def __init__(self, layout, pos, dest, frame, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.dest = dest
        self.layout = layout
        self.frame = frame
        self.color = frame.type.value
        self.layout.add_widget(self)
        angle = Vector(0, 1).angle(
            (pos[0] - dest.pos[0], dest.pos[1] - pos[1]))
        self.vel = Vector(0, 15).rotate(angle)
        self.event = Clock.schedule_interval(self.move, 0.5)

    def move(self, dt):
        if Vector(self.pos).distance2(self.dest.pos) > 100:
            self.pos = Vector(*self.pos) + self.vel
        else:
            self.layout.remove_widget(self)
            self.dest.receive(self.frame)
            Clock.unschedule(self.event)

    def show_frame(self):
        FrameInfo(self.frame)


class FrameInfo(Popup):
    topic = StringProperty()
    ttl = StringProperty()
    message = StringProperty()
    type_ = StringProperty()

    def __init__(self, frame, **kwargs):
        super().__init__(**kwargs)
        self.topic = frame.topic
        self.ttl = str(frame.ttl)
        self.message = frame.content.name
        self.type_ = frame.type.name
        self.open()
