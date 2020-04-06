"""
Module describes logic of actions, that could perform element.
All models are divided on two types:
 - Generic
 - Specific

 Generic models - are models, that perform the same actions for different types of elements.
 Example of such model is receiver, that for each element do the same: listen  for frames, and tries to identify 
 if this frame  came to him. Implementations of such models should be placed in `models/generic` folder.

 Another type of models are specific ones.An example is a software for light, that describes what 
 how to change saturation or hue. This model is specific only for light, because nothing except light 
 could perform such actions.
 Models of such types should be placed in folders with name model/NAME_OF_ELEMENT_model.
 Model from previous example will be placed in folder
    model/light_models
"""
