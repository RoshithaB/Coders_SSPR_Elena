import math
import osmnx  as ox
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import *
from . import AbstractAlgorithm
import networkx as nx
from src.utils import calculate_astar_path, ElevationGain, ElevationStrategy
from src.utils import Constants, RouteAlgorithms

class DijsktraController(AbstractAlgorithm.AbstractAlgorithm):
"""
This is the class representing a Dijkstra based controller for route calculations.
This controller uses the dijkstra's algorithm to calculate routes
with considerations for elevation gain, path limit and scaling factor.
"""
    def set_contents(self, graph, origin, destination, path_limit, scaling_factor, elevation_strategy, short_dist):
        # set the origin of the route
        self.set_origin(origin)  

        # set the destination of the route
        self.set_destination(destination) 

        # set the elevation strategy
        self.set_elevation_strategy(elevation_strategy) 

        #set the path limit
        self.path_limit = path_limit 

        # set the scaling factor
        self.scaling_factor = scaling_factor 

        # set the graph map
        self.graph_map = graph 

        # initialize the elevation path as NONE
        self.elevation_path = None 

        # Create new algorithmmodel instance
        self.model = AlgorithmModel() 

        # Set the shortest distance
        self.shortest_dist = short_dist 

        # set the elevation gain
        self.elevation_gain = short_dist.get_gain() 

        # Set the algorithm
        self.set_algo()

    # set algo as DIJKSTRA_ALGORITHM
    def set_algo(self):
        self._algo = RouteAlgorithms.DIJKSTRA_ALGORITHM.value

    # return the algo
    def get_algo(self):
        return self._algo

    # set the elevation strategy
    def set_elevation_strategy(self, elevation_strategy):
        self._elevation_strategy = elevation_strategy

    # return elevation strategy 
    def get_elevation_strategy(self):
        return self._elevation_strategy

    # set origin of the route
    def set_origin(self, origin):
        self._origin = origin

    # return the origin of the route
    def get_origin(self):
        return self._origin

    # set  destination of the route
    def set_destination(self, destination):
        self._destination = destination

    # return the destination of the route
    def get_destination(self):
        return self._destination

    # Clculate the elevation path using Dijkstra's algo
    def calculate_elevation_path(self):
        return nx.shortest_path(self.graph_map, source=self._origin, target=self._destination,
                                                weight=Constants.LENGTH.value)

    # Initialise minmax as 1  and check if elevationstrategy is max and set minmax as -1
    def set_minmax(self):
        self.minmax = 1
        if self._elevation_strategy == ElevationStrategy.MAX.value:
            self.minmax = -1

    # create new pathmodel imstace and set algo in path model and 
    # set the elevation gain in the path model
    # set the dro as 0
    # set the path in the path model
    # set the distance in the path model 
    # return the path model
    def set_path_contents(self):
        path_model = PathModel()
        path_model.set_algo(RouteAlgorithms.DIJKSTRA_ALGORITHM.value)
        path_model.set_elevation_gain(self.model.get_path_weight(self.graph_map, self.elevation_path, ElevationGain.ELEVATION_GAIN.value))
        path_model.set_drop(0)
        path_model.set_path([[self.graph_map.nodes[route_node]['x'], self.graph_map.nodes[route_node]['y']]
                                            for route_node in self.elevation_path])
        path_model.set_distance(
            sum(ox.utils_graph.get_route_edge_attributes(self.graph_map, self.elevation_path, Constants.LENGTH.value)))
        return path_model

    # set the minmax value
    # calculate the elevation path usingg Dijkstra's algorithm
    def fetch_route_with_elevation(self):
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
                                              source=self._origin,
                                              target=self._destination,
                                              heuristic= None,
                                              weight=weight)
            elev_distance = sum(ox.utils_graph.get_route_edge_attributes(self.graph_map, elev_path, Constants.LENGTH.value))
            elev_gain = self.model.get_path_weight(self.graph_map, elev_path, ElevationGain.ELEVATION_GAIN.value)
            if elev_distance <= (self.path_limit) * self.shortest_dist.get_distance() and \
                    self.minmax * elev_gain <= self.minmax * self.elevation_gain:
                self.elevation_path = elev_path
                self.elevation_gain = elev_gain
            self.scaling_factor *= 5
        return self.set_path_contents()