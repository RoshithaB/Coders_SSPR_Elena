import math
import osmnx  as ox
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import *
from . import AbstractAlgorithm
import networkx as nx
from src.utils import calculate_astar_path, ElevationGain, ElevationStrategy
from src.utils import Constants, RouteAlgorithms

class DijsktraController(AbstractAlgorithm.AbstractAlgorithm):

    def set_contents(self, graph, origin, destination, path_limit, scaling_factor, elevation_strategy, short_dist):
        self.set_origin(origin)
        self.set_destination(destination)
        self.set_elevation_strategy(elevation_strategy)
        self.path_limit = path_limit
        self.scaling_factor = scaling_factor
        self.graph_map = graph
        self.elevation_path = None
        self.model = AlgorithmModel()
        self.shortest_dist = short_dist
        self.elevation_gain = short_dist.get_gain()
        self.set_algo()

    def set_algo(self):
        self._algo = RouteAlgorithms.DIJKSTRA_ALGORITHM.value

    def get_algo(self):
        return self._algo
    
    def set_elevation_strategy(self, elevation_strategy):
        self._elevation_strategy = elevation_strategy
    
    def get_elevation_strategy(self):
        return self._elevation_strategy
    
    def set_origin(self, origin):
        self._origin = origin
    
    def get_origin(self):
        return self._origin
    
    def set_destination(self, destination):
        self._destination = destination
    
    def get_destination(self):
        return self._destination
    
    def calculate_elevation_path(self):
        return nx.shortest_path(self.graph_map, source=self._origin, target=self._destination,
                                                weight=Constants.LENGTH.value)
    
    def set_minmax(self):
        self.minmax = 1
        if self._elevation_strategy == ElevationStrategy.MAX.value:
            self.minmax = -1

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