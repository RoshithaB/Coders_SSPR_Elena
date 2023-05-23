from networkx.algorithms.shortest_paths.weighted import _weight_function
from itertools import count
from heapq import heappush, heappop
import networkx as nx
from enum import Enum

class ElevationGain(Enum):
    """
    Enumeration for elevation gain options
    """
    ELEVATION_GAIN = "elevation_gain"
    NORMAL = "normal"

class ElevationStrategy(Enum):
    """
    Enumeration for elevationstrategy options
    """
    MIN = "min"
    MAX = "max"
    NONE = "None"

class Constants(Enum):
    """
    Enumeration for constant values
    """
    LENGTH = "length"
    WEIGHT = "weight"
    ELEVATION = "elevation"
    GOOGLEMAPS_CLIENT_KEY = "AIzaSyCJRDo3QnMDZo_UApNI9GnmODzHw-zWtHw"

class RouteAlgorithms(Enum):
    """
    Enumeration for Route algorithms
    """
    ASTAR_ALGORITHM = "A* Algorithm."
    DIJKSTRA_ALGORITHM = "Dijkstra Algorithm."
    SHORTEST_ROUTE_ALGORITHM = "Shortest Route Algorithm."

def calculate_astar_path(G, source, target, heuristic, weight):
    """
    Calculate the shortest path using A* Algorithm

    Return:
        shortest path from source to target.
    """
    if source not in G or target not in G:
        return

    if heuristic is None:
        heuristic = lambda u, v: 0
            
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