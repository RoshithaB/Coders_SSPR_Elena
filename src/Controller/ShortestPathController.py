import networkx as nx
import osmnx as ox
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import PathModel
from src.Model.Observable import Observable
from src.utils import Constants, ElevationGain, ElevationStrategy
from src.utils import RouteAlgorithms
from . import AbstractAlgorithm
import logging
import os

ELEVATION_GAIN = "elevation_gain"
LENGTH = "length"

# Configure the logger
log_file = os.path.join("..", "logging.txt")
logging.basicConfig(filename=log_file, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ShortestPathController(AbstractAlgorithm.AbstractAlgorithm):
    """
    This is the class with methods for calculating the shortest distance between two nodes.
    """
    def __init__(self):
        """
        Initializes the ShortestPathController object
        """
        self.G = None
        self.shortest_path = None
        self.shortest_dist = None
        self.start_location = None
        self.end_location = None
        self.model = AlgorithmModel()

    # set origin of the route
    def set_origin(self, origin):
        logger.debug("Origin is set on controller.")
        self._origin = origin

    # return the origin of the route
    def get_origin(self):
        return self._origin

    # set  destination of the route
    def set_destination(self, destination):
        logger.debug("Destination is set on controller.")
        self._destination = destination

    # return the destination of the route
    def get_destination(self):
        return self._destination
    
    # Sets the graph for calculating the shortest path
    def set_graph(self, G):
        logger.debug("Graph is set in Shortest Path Controller.")
        self.G = G

    # set algo as DIJKSTRA_ALGORITHM
    def set_algo(self):
        logger.debug("Algorithm is set on controller.")
        self._algo = RouteAlgorithms.SHORTEST_ROUTE_ALGORITHM.value

    # return the algo
    def get_algo(self):
        return self._algo
    
    # set the elevation strategy
    def set_elevation_strategy(self, elevation_strategy):
        logger.debug("Elevation strategy is set on controller.")
        self._elevation_strategy = ElevationStrategy.NONE.value

    # return elevation strategy 
    def get_elevation_strategy(self):
        return self._elevation_strategy

    # sets the contents of the path with calculated data
    def set_path_contents(self):
        path_model = PathModel()
        path_model.set_algo(RouteAlgorithms.SHORTEST_ROUTE_ALGORITHM.value)
        path_model.set_start_location(self.start_location)
        path_model.set_end_location(self.end_location)
        path_model.set_elevation_gain(self.model.get_path_weight(self.G, self.shortest_path, ElevationGain.ELEVATION_GAIN.value))
        path_model.set_drop(0)
        
        path_model.set_path([[self.G.nodes[node]['x'], self.G.nodes[node]['y']]
                                            for node in self.shortest_path])
            
        self.shortest_dist = sum(ox.utils_graph.get_route_edge_attributes(self.G,self.shortest_path, Constants.LENGTH.value))
        path_model.set_distance(self.shortest_dist)
        logger.debug("Path Model attributes are set.")
        return path_model

    # calculates the shortest path between two nodes
    def get_shortest_path(self, start, end):
        
        self.start_location, _ = ox.get_nearest_node(self.G, point=start, return_dist=True)
        self.end_location, _ = ox.get_nearest_node(self.G, point=end, return_dist=True)
        self.shortest_path = nx.shortest_path(self.G, self.start_location, self.end_location, weight=Constants.LENGTH.value)

        
        return self.set_path_contents()
