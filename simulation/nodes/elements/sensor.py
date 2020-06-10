from . import Element
from datetime import datetime
#import time
import datetime as dt
from simulation.environment import Environment
from simulation.network import Content


class Sensor(Element):
    def __init__(self, content, node):
        super().__init__(content, node, use_scheduler=True)
        light_on = content['time_on'].split(":")
        light_off = content['time_off'].split(":")
        self.on = dt.datetime.now().replace(hour=int(light_on[0]), minute=int(light_on[1]), second=0, microsecond=0).\
            time()
        self.off = dt.datetime.now().replace(hour=int(light_off[0]), minute=int(light_off[1]), second=0, microsecond=0).\
            time()

    def do_action(self, dt):
        time = Environment.time
        if self.on <= time < self.off:
            self.send(Content.LIGHT_ON)
        else:
            self.send(Content.LIGHT_OFF)
