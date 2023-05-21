import math
import osmnx as ox
from heapq import heappush, heappop
from itertools import count
from networkx.algorithms.shortest_paths.weighted import _weight_function
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import *
import networkx as nx

MAXIMIZE = "max"
MINIMIZE = "min"
EMPTY = "empty"
ELEVATION_GAIN = "elevation_gain"
LENGTH = "length"

class AlgorithmController():
    """
    Controller Class to compute the shortest path with elevation using the chosen algorithm.
    """
    def __init__(self, graph, shortest_dist, path_limit, elevation_strategy, origin, destination, elevation_gain, algo_flag):
        self.graph = graph
        self.origin = origin
        self.destination = destination
        self.elevation_path = None
        self.shortest_dist = shortest_dist
        self.path_limit = path_limit
        self.elevation_strategy = elevation_strategy
        self.elevation_gain = elevation_gain
        self.algo_flag = algo_flag
        self.scaling_factor = 100
        self.model = AlgorithmModel()

    def heuristic_calc(self, a, b):
        return self.graph.nodes[a]['dist_from_dest'] * 1 / self.scaling_factor

    def calculate_elevation_path(self, G, source, target, heuristic, weight):
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

    def fetch_route_with_elevation(self):
        minmax = 1 if self.elevation_strategy == MINIMIZE else -1
        self.elevation_path = nx.shortest_path(self.graph, source=self.origin, target=self.destination,
                                                weight=LENGTH)
        heurestic_val = None
        while self.scaling_factor < 10000:
            elevation_path = self.calculate_elevation_path(self.graph,
                                              source=self.origin,
                                              target=self.destination,
                                              heuristic= heurestic_val,
                                              weight=lambda u, v, d:
                                              math.exp(minmax * d[0][LENGTH] * (
                                                          d[0]['grade'] + d[0]['grade_abs']) / 2)
                                              + math.exp((1 / self.scaling_factor) * d[0][LENGTH]))
            elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(self.graph, elevation_path, LENGTH))
            elevation_gain = self.model.get_path_weight(self.graph, elevation_path, ELEVATION_GAIN)
            if elevation_distance <= (self.path_limit) * self.shortest_dist and \
                    minmax * elevation_gain <= minmax * self.elevation_gain:
                self.elevation_path = elevation_path
                self.elevation_gain = elevation_gain
            self.scaling_factor *= 5
        path_model = PathModel()
        path_model.set_algo("A* Algorithm.")
        path_model.set_elevation_gain(self.model.get_path_weight(self.graph, self.elevation_path, ELEVATION_GAIN))
        path_model.set_drop(0)
        path_model.set_path([[self.graph.nodes[route_node]['x'], self.graph.nodes[route_node]['y']]
                                            for route_node in self.elevation_path])
        path_model.set_distance(
            sum(ox.utils_graph.get_route_edge_attributes(self.graph, self.elevation_path, LENGTH)))
        path_model.set_path_flag(2)

        return path_model


        

