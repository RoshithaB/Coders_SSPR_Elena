import math
import osmnx  as ox
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import *
from . import AbstractAlgorithm
import networkx as nx
from src.utils import calculate_astar_path


class AStarController(AbstractAlgorithm.AbstractAlgorithm):
    def set_contents(self, graph, origin, destination, heuristic, path_limit, scaling_factor, elevation_strategy, short_dist):
        self.graph_map = graph
        self.origin = origin
        self.destination = destination
        self.heuristic = heuristic
        self.path_limit = path_limit
        self.scaling_factor = scaling_factor
        self.elevation_strategy = elevation_strategy
        self.elevation_path = None
        self.model = AlgorithmModel()
        self.shortest_dist = short_dist
        self.elevation_gain = short_dist.get_gain()

    def dist(self, a, b):
        return self.graph_map.nodes[a]['dist_from_dest'] * 1 / self.scaling_factor

    def set_algo(self, algo):
        self.algo = algo

    def get_algo(self):
        return self.algo

    def get_elevation_strategy(self):
        return self.elevation_strategy
    
    def set_scaling_factor(self):
        self.scaling_factor = 100

    def get_scaling_factor(self):
        return self.scaling_factor

    def calculate_elevation_path(self):
        return nx.shortest_path(self.graph_map, source=self.origin, target=self.destination,
                                                weight="length")
    
    def set_elevation_strategy(self):
        self.minmax = 1
        if self.elevation_strategy == 'max':
            self.minmax = -1
        
    def set_path_contents(self):
        path_model = PathModel()
        path_model.set_algo("A* Algorithm.")
        path_model.set_elevation_gain(self.model.get_path_weight(self.graph_map, self.elevation_path, "elevation_gain"))
        path_model.set_drop(0)
        path_model.set_path([[self.graph_map.nodes[route_node]['x'], self.graph_map.nodes[route_node]['y']]
                                            for route_node in self.elevation_path])
        path_model.set_distance(
            sum(ox.utils_graph.get_route_edge_attributes(self.graph_map, self.elevation_path, "length")))
        path_model.set_path_flag(2)
        return path_model

    def fetch_route_with_elevation(self):
        self.set_elevation_strategy()
        self.elevation_path = self.calculate_elevation_path()

        while self.scaling_factor < 10000:
            elevation_path = calculate_astar_path(self.graph_map,
                                              source=self.origin,
                                              target=self.destination,
                                              heuristic= self.dist,
                                              weight=lambda u, v, d:
                                              math.exp(self.minmax * d[0]['length'] * (
                                                          d[0]['grade'] + d[0]['grade_abs']) / 2)
                                              + math.exp((1 / self.scaling_factor) * d[0]["length"]))
            elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(self.graph_map, elevation_path, "length"))
            elevation_gain = self.model.get_path_weight(self.graph_map, elevation_path, "elevation_gain")
            if elevation_distance <= (self.path_limit) * self.shortest_dist.get_distance() and \
                    self.minmax * elevation_gain <= self.minmax * self.elevation_gain:
                self.elevation_path = elevation_path
                self.elevation_gain = elevation_gain
            self.scaling_factor *= 5
        return self.set_path_contents()
