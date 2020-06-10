import datetime as dt
import time


class Environment:
    """
    Class which should state of world.

    Provide interface to interaction between nodes and elements.
    """
    temperature = 30
    humidity = 0
    illuminance = 0
    heaters = []
    time = dt.datetime.now().time()
    delta = dt.timedelta(minutes=1)

    @staticmethod
    def heat():
        """
        Affect temperature and humidity.
        """
        # if zero heaters, than temperature will decrease
        coeficient = len(Environment.heaters) - 1
        Environment.temperature += coeficient * 0.1

    @staticmethod
    def turn_light():
        """
        Affect illuminance
        """
        pass

    @staticmethod
    def set_time():
        Environment.time = (dt.datetime.combine(dt.date(1, 1, 1), Environment.time) + Environment.delta).time()
        #Environment.time = (datetime.combine(datetime.date(1, 1, 1), Environment.time) + delta).time()
        #Environment.time += timedelta(minutes=1)
