from abc import abstractmethod
from src import *
from abc import ABC, abstractmethod
from src.Model import Observable

"""
    Interface defining an Observer.
"""
class Observer:

    """
       Update method for when the current state changes.
       @param observable = observable whose state is changed.
    """
    @abstractmethod
    def update(self, observable):
        pass