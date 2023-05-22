
from abc import ABC
from abc import abstractmethod

class AbstractAlgorithm(ABC):
    def __init__(self):
        self.model = None
        self._origin = None
        self._destination = None
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
    def set_elevation_strategy(self, elevation_strategy):
        pass
    
    @abstractmethod
    def get_elevation_strategy(self):
        pass

    @abstractmethod
    def set_origin(self, origin):
        pass

    @abstractmethod
    def set_destination(self, destination):
        pass

    @abstractmethod
    def get_origin(self, origin):
        pass

    @abstractmethod
    def get_destination(self, destination):
        pass