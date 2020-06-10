from simulation.network import Content, Frame, Type
from simulation.nodes.features import Relay
from kivy.clock import Clock


class Element:
    registered_elements = {}

    def __init__(self, content, node, use_scheduler=False):
        """
        :param content: dict of form
        {
            'device': self.device,
            'publishing': self.publishing,
            'subcribed': self.subcribed,
            'role'
        }
        """
        self._batery_level = 1
        self.publishing = content['publishing']
        self.subscribed = content['subcribed']
        if content.setdefault('role', '').lower() == 'relay':
            self.role = Relay(self)
        else:
            self.role = None
        self.node = node
        self.scheduler = None
        if use_scheduler:
            self.scheduler = Clock.schedule_interval(self.do_action, 2)

    def __init_subclass__(cls):
        """Register created elements"""
        Element.registered_elements[str.lower(cls.__name__)] = cls

    @staticmethod
    def from_name(class_name):
        return Element.registered_elements[class_name]()

    def receive(self, frame):
        """
        Checks if it should receive a frame
        """
        if frame.topic in self.subscribed or (self.role and type(self.role) == Relay) and not (frame.topic == self.publishing and frame.type == Type.RELAYED):
            if self.role:
                self.role.on_receive(frame)
            else:
                self.on_receive(frame)

    def do_action(self):
        """
        Scheduled by scheduler.
        """

    def on_receive(self, frame):
        """
        Called on successfull frame receive.
        """

    def send(self, message: Content, ttl=11):
        frame=Frame(self.publishing, ttl, message)
        self.node.send(frame)

    def on_remove(self):
        if self.scheduler:
            Clock.unschedule(self.scheduler)
