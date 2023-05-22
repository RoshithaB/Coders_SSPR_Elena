#This is the observable model
from src.Model import *

class Observable:
    """
         All methods of an observable are contained in this class.
    """
    def __init__(self):
        self.isStateChange = False #flag to keep track of state change.
        self.observers = set() #The set of observers that subscribe to be notified.
    
    """
        Register an observer
       @param obs = observer tp register.
    """
    def register(self, obs):
        self.observers.add(obs)
    
    """
        Unregister a registered observer
        @param obs = observer to unregister
    """
    def unegister(self, obs):
        self.observers.remove(obs)
    
    """
        Method to alert all observers when a state changes.
    """
    def state_changed(self):
        pass

    """
        To get current state
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
