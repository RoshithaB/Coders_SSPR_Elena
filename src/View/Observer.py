from abc import abstractmethod
from src import *
from abc import ABC, abstractmethod
from src.Model import Observable

"""
    An observer's interface is defined.
"""
class Observer:

    """
    A method of updating the current state when it changes
    observable is an observable whose state has changed.
    """
    @abstractmethod
    def update(self, observable):
        """
        Update method for when the current state changes.
        """
        pass