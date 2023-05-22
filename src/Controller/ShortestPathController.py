import networkx as nx
import osmnx as ox
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import PathModel
from src.Model.Observable import Observable
from src.utils import Constants, ElevationGain
from src.utils import RouteAlgorithms

ELEVATION_GAIN = "elevation_gain"
LENGTH = "length"

class ShortestPathController:
    """
    Class consisting of methods to get the shortest path between two nodes.
    """
    def __init__(self):
        self.G = None
        self.shortest_path = None
        self.shortest_dist = None
        self.start_location = None
        self.end_location = None
        self.model = AlgorithmModel()

    def set_graph(self, G):
        self.G = G

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
        return path_model

    def get_shortest_path(self, start, end):
        """
        Method to compute shortest path using weights on the edges.
        """
        self.start_location, _ = ox.get_nearest_node(self.G, point=start, return_dist=True)
        self.end_location, _ = ox.get_nearest_node(self.G, point=end, return_dist=True)
        self.shortest_path = nx.shortest_path(self.G, self.start_location, self.end_location, weight=Constants.LENGTH.value)

        
        return self.set_path_contents()
