"""
Module contain, implementations of existing elements.

An element - is a physical object, from which nodes are created.
Element could be for example light, switch, termostat, light, etc.
Each element consists have models installed on it, and also it has some logic, 
that describes interaction of this element with environment.
"""
from .element import Element
from .temperature_tracker import TemperatureTracker
