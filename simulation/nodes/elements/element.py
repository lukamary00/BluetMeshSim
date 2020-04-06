from abc import ABC, abstractmethod


class Element(ABC):
    # dict with all registered elements
    reg_elements = {}

    def __init__(self):
        pass

    @abstractmethod
    def notify(self, environment_variable_value):
        pass

    def __init_subclass__(cls):
        """Register all elements"""
        Element.reg_elements[str.lower(cls.__name__)] = cls

    @staticmethod
    def from_name(class_name, env):
        return Element.reg_elements[class_name](env)
