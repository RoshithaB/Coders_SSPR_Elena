
from abc import ABC
from abc import abstractmethod

class AbstractAlgorithm(ABC):
    """
    This is an AbstractAlgorithm class representing an algorithm interface
    """
    def __init__(self):
        
        self.model = None
        self._origin = None
        self._destination = None
        self.graph_map = None
        self._elevation_strategy = None
        self._algo = None

    # set the algorithm for path calculation
    @abstractmethod
    def set_algo(algorithm):
        pass

    # Get the algorithm used for path calculation
    @abstractmethod
    def get_algo():
        pass
    
    # Set the elevation_strategy for path calculation
    @abstractmethod
    def set_elevation_strategy(self, elevation_strategy):
        pass
    
    # get the elevation_strategy used for path calculation
    @abstractmethod
    def get_elevation_strategy(self):
        pass

    # set the origin of the path
    @abstractmethod
    def set_origin(self, origin):
        pass

    # Set the destination of the path 
    @abstractmethod
    def set_destination(self, destination):
        pass


    # Get the origin of the path
    @abstractmethod
    def get_origin(self, origin):
        pass

    # Get the destination of the path
    @abstractmethod
    def get_destination(self, destination):
        pass