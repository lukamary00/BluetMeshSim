from simulation.nodes.elements import Element

class TemperatureTracker(Element):
    def __init__(self, env):
        self.__threshold = None
        self.__env = env

    @property
    def threshold(self):
        return self.__threshold

    @threshold.setter
    def threshold(self, value):
        self.__threshold = value

    def notify(self, newvalue):
        if newvalue > self.__threshold:
            print("newvalue > threshhold")









