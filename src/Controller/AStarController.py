import math
import osmnx  as ox
from networkx.algorithms.shortest_paths.weighted import _weight_function
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import *
from . import AbstractAlgorithm
import networkx as nx
from heapq import heappush, heappop
from itertools import count

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

    def calculate_astar_path(self, G, source, target, heuristic, weight):
        if source not in G or target not in G:
            return

        if heuristic is None:
            def heuristic(u, v):
                return 0
            
        weight = _weight_function(G, weight)
        cnt = count()
        queue = [(0, next(cnt), source, 0, None)]
        enqueued, explored = {}, {}
        while queue:
            _, __, current, distance, parent = heappop(queue)
            if current == target:
                path = [current]
                node = parent
                while node is not None:
                    path.append(node)
                    node = explored[node]
                path.reverse()
                return path
            if current in explored:
                if explored[current] is None:
                    continue
                qcost, h = enqueued[current]
                if qcost < distance:
                    continue
            explored[current] = parent
            for neighbor, w in G[current].items():
                cost = distance + weight(current, neighbor, w)
                if neighbor in enqueued:
                    qcost, h = enqueued[neighbor]
                    if qcost <= cost:
                        continue
                else:
                    h = heuristic(neighbor, target)
                enqueued[neighbor] = cost, h
                heappush(queue, (cost + h, next(cnt), neighbor, cost, current))
        raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")

    def calculate_elevation_path(self):
        return nx.shortest_path(self.graph_map, source=self.origin, target=self.destination,
                                                weight="length")
    
    def set_elevation_strategy(self):
        self.minmax = 1
        if self.elevation_strategy == 'max':
            print("HEy")
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
            elevation_path = self.calculate_astar_path(self.graph_map,
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
