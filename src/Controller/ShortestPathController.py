import networkx as nx
import osmnx as ox
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import PathModel
from src.Model.Observable import Observable

ELEVATION_GAIN = "elevation_gain"
SHORTEST = "Shortest Route"
LENGTH = "length"

class ShortestPathController:
    """
    Class consisting of methods to get the shortest path between two nodes.
    """
    def __init__(self, G):
        self.G = G
        self.shortest_path = None
        self.shortest_dist = None
        self.start_location = None
        self.end_location = None
        self.model = AlgorithmModel()

    def get_shortest_path(self, start, end):
        """
        Method to compute shortest path using weights on the edges.
        """
        self.start_location, _ = ox.distance.nearest_nodes(self.G, start[0], start[1], return_dist=True)
        self.end_location, _ = ox.distance.nearest_nodes(self.G, end[0], end[1], return_dist=True)
        self.shortest_path = nx.shortest_path(self.G, self.start_location, self.end_location, weight=LENGTH)

        path_model = PathModel()
        path_model.set_algo(SHORTEST)
        path_model.set_start_location(self.start_location)
        path_model.set_end_location(self.end_location)
        path_model.set_elevation_gain(self.model.get_path_weight(self.G, self.shortest_path, ELEVATION_GAIN))
        path_model.set_drop(0)
        
        path_model.set_path([[self.G.nodes[node]['x'], self.G.nodes[node]['y']]
                                            for node in self.shortest_path])
            
        self.shortest_dist = sum(ox.utils_graph.get_route_edge_attributes(self.G,self.shortest_path,LENGTH))
        print(f"\n\nshortest_distance = {self.shortest_dist}\n\n")
        path_model.set_distance(self.shortest_dist)
        path_model.set_path_flag(1)
        return path_model
