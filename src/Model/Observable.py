
from src.Model import *

class Observable:
    """
        This is an Abstract class for all methods of an Observable
    """
    def __init__(self):
        self.isStateChange = False #flag to keep track of state change.
        self.observers = set() #The set of observers that subscribe to be notified.
    
    """
        Register an observer
       @param obs = observer that needs to be registered
    """
    def register(self, obs):
        self.observers.add(obs)
    
    """
        Unregister a registered observer
        @param obs = observer that needs to be unregistered
    """
    def unegister(self, obs):
        self.observers.remove(obs)
    
    """
        Method to notify all observers when a state is changed
    """
    def state_changed(self):
        pass

    """
        To get the current state
        @return current state flag
    """
    def get_state(self):
        return self.isStateChange

    """
        To set the current state to true
        @param state = current state
    """
    def set_state(self, state):
        self.isStateChange = state
