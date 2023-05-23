#Controller for AStar
import math
import osmnx  as ox
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import *
from . import AbstractAlgorithm
import networkx as nx
from src.utils import calculate_astar_path, ElevationGain, ElevationStrategy
from src.utils import Constants, RouteAlgorithms


class AStarController(AbstractAlgorithm.AbstractAlgorithm):
    """
    This is the class representing a AStar based controller for route calculations.
    """
    def set_contents(self, graph, origin, destination, heuristic, path_limit, scaling_factor, elevation_strategy, short_dist):
        """
        Sets the contents required for AStar Algorithm

        Returns:
            NONE
        """
        # set the origin of the route
        self.set_origin(origin)
        # set the destination of the route
        self.set_destination(destination)
        # set the elevation strategy
        self.set_elevation_strategy(elevation_strategy)
        self.heuristic = heuristic
        #set the path limit
        self.path_limit = path_limit
        # set the scaling factor
        self.scaling_factor = scaling_factor
        # set the graph map
        self.graph_map = graph
        self.elevation_path = None

        # Create new algorithmmodel instance
        self.model = AlgorithmModel()
        self.model.set_elevation_strategy(self.get_elevation_strategy())
        self.shortest_dist = short_dist
        self.elevation_gain = short_dist.get_gain()
        self.set_algo()

    # sets the algorithm for A*
    def set_algo(self):
        self._algo = RouteAlgorithms.ASTAR_ALGORITHM.value

    # Returns the algorithm used
    def get_algo(self):
        return self._algo
    
    # Sets the elevation_strategy
    def set_elevation_strategy(self, elevation_strategy):
        self._elevation_strategy = elevation_strategy
    
    # sets the monmax value based on elevation_strategy
    def set_minmax(self):
        self.minmax = 1
        if self._elevation_strategy == ElevationStrategy.MAX.value:
            self.minmax = -1

    # Returns the elevation_strategy
    def get_elevation_strategy(self):
        return self._elevation_strategy
    
    # sets the path origin
    def set_origin(self, origin):
        self._origin = origin
    
    # returns the origin of the path
    def get_origin(self):
        return self._origin
    
    # sets the destination of the path
    def set_destination(self, destination):
        self._destination = destination
    
    # returns the destination of the path
    def get_destination(self):
        return self._destination
    
    # set the model
    def set_model(self, model):
        self.model = model
        self.model.set_elevation_strategy(self.get_elevation_strategy())
    
    def dist(self, a, b):
        """
        Calculates the distance between the two nodes

        Args:
            a: The first node
            b: The second node

        Returns:
            The distance between the nodes.
        """
        return self.graph_map.nodes[a]['dist_from_dest'] * 1 / self.scaling_factor

  
    def calculate_elevation_path(self):
        """
        Calculates the elevation_path using the A* algorithm

        Returns:
            The elevation path
        """
        return nx.shortest_path(self.graph_map, source=self._origin, target=self._destination,
                                                weight=Constants.LENGTH.value)
    
    # Sets the contents of the path model
    def set_path_contents(self):
        path_model = PathModel()
        path_model.set_algo(RouteAlgorithms.ASTAR_ALGORITHM.value)
        path_model.set_elevation_gain(self.model.get_path_weight(self.graph_map, self.elevation_path, ElevationGain.ELEVATION_GAIN.value))
        path_model.set_drop(0)
        path_model.set_path([[self.graph_map.nodes[route_node]['x'], self.graph_map.nodes[route_node]['y']]
                                            for route_node in self.elevation_path])
        path_model.set_distance(
            sum(ox.utils_graph.get_route_edge_attributes(self.graph_map, self.elevation_path, Constants.LENGTH.value)))
        # Returns the path model
        return path_model

    def fetch_route_with_elevation(self):
        """
        Fetches the route with elevation

        Returns:
            The path model
        """
        self.set_minmax()
        self.elevation_path = self.calculate_elevation_path()

        while self.scaling_factor < 10000:
            weight = lambda u, v, d: math.exp(self.minmax \
                    * d[0]['length'] \
                    * (d[0]['grade'] \
                    + d[0]['grade_abs']) / 2) \
                    + math.exp((1 / self.scaling_factor) \
                    * d[0][Constants.LENGTH.value])

            elev_path = calculate_astar_path(self.graph_map,
                                              source=self.get_origin(),
                                              target=self.get_destination(),
                                              heuristic=self.dist,
                                              weight=weight)
            elev_dist = sum(ox.utils_graph.get_route_edge_attributes(self.graph_map, elev_path, Constants.LENGTH.value))
            elev_gain = self.model.get_path_weight(self.graph_map, elev_path, ElevationGain.ELEVATION_GAIN.value)
            if elev_dist <= (self.path_limit) * self.shortest_dist.get_distance() and \
                    self.minmax * elev_gain <= self.minmax * self.elevation_gain:
                self.elevation_path = elev_path
                self.elevation_gain = elev_gain
            self.scaling_factor *= 5
        return self.set_path_contents()
