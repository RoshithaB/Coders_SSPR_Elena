
from abc import ABC
from abc import abstractmethod

class AbstractAlgorithm(ABC):
    def __init__(self):
        self.model = None
        self.origin = None
        self.destination = None
        self.graph_map = None
        self._elevation_strategy = None
        self._algo = None

    @abstractmethod
    def set_algo(algorithm):
        pass

    @abstractmethod
    def get_algo():
        pass
        
    @abstractmethod
    def set_elevation_strategy(self):
        pass
    
    @abstractmethod
    def get_elevation_strategy(self):
        pass
    
    @abstractmethod
    def set_scaling_factor(self):
        pass

    @abstractmethod
    def get_scaling_factor(self):
        pass