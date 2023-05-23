from src.Model.Observable import Observable
import logging
import os

# Configure the logger
log_file = os.path.join("..", "logging.txt")
logging.basicConfig(filename=log_file, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PathModel(Observable):
    """
    Class that consists of getter and setter methods for path attributes.
    """
    def __init__(self):
        super().__init__()
        self.algo = ""
        self.gain = 0
        self.drop = 0
        self.path = []
        self.distance = 0.0
        self.origin = None, None
        self.destination = None, None
        self.observers = set() #The set of observers that subscribe to be notified.
    
    """
        Register an observer
        @param obs = observer to register
    """
    def register(self, obs):
        self.observers.add(obs)
    
    """
        Unregister a registered observer
        @param obs = observer to unregister
    """
    def unegister(self, obs):
        self.observers.remove(obs) 
        
    # set algorithm to given value and notify observers that the state has changed
    def set_algo(self, algo):
        self.algo = algo
        logger.debug("Algorithm is set for Path Model.")
        self.state_changed()

    # Set the elevation gain to given value and notify the 
    # observers that the state has changed
    def set_elevation_gain(self, gain):
        self.gain = gain
        logger.debug("Elevation gain is set for Path Model.")
        self.state_changed()

    # Set the drop to the given value and notify the observers of the state change
    def set_drop(self, drop):
        self.drop = drop
        self.state_changed()

    # set the path to the given value and notify the state change
    def set_path(self, path):
        self.path = path
        logger.debug("Path is set for Path Model.")
        self.state_changed()

    # set the distance to the given value and notify the state change
    def set_distance(self, distance):
        self.distance = distance
        logger.debug("Distance is set for Path Model.")
        self.state_changed()

    # return the algorithm
    def get_algo(self):
        return self.algo
    
    # retuen the elevation gain
    def get_gain(self):
        return self.gain
    
    # return the drop
    def get_drop(self):
        return self.drop
    
    # return the path 
    def get_path(self):
        return self.path
    
    # return the distance
    def get_distance(self):
        return self.distance
    
    # set start location to given value  and notify the state change
    def set_start_location(self, origin):
        self.origin = origin
        logger.debug("Start location is set for Path Model.")
        self.state_changed()

    # return the start ocation
    def get_origin(self):
        return self.origin
    # set the end location to the given value and notify the state change
    def set_end_location(self, destination):
        self.destination = destination
        logger.debug("Final location is set for Path Model.")
        self.state_changed()
    
    # return the end location
    def get_destination(self):
        return self.destination

    # Iterate overall observers
    def state_changed(self):
        logger.debug("State is change in Path Model.")
        for observer in self.observers:
            observer.update(self)
