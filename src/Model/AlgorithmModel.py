from src.utils import ElevationGain

LENGTH = "length"
WEIGHT = "weight"
ELEVATION = "elevation"


class AlgorithmModel:
    """
    Critical parameters like the graph, algorithm, path_limit etc are initialized by this class. 
    It has methods for registering observers, setting algorithms, setting algorithm objects, 
    printing route data and notifying observers, among other things. 
    """

    def __init__(self):
        """
        The route and algorithm attributes are initialized by this method.
        """
        self._graph = None
        self._observer = None
        self._algorithm = None
        self._path_limit = None
        self._elevation_strategy = None
        self._heuristic = None

    # set graph to given value
    def set_graph(self, graph):
        self.graph = graph

    # return the graph
    def get_graph(self):
        return self.graph
    
    # Set path limit to given value
    def set_path_limit(self, path_limit):
        self.path_limit = path_limit

    # return the path limit
    def get_path_limit(self):
        return self.path_limit
    
    # Set elevation strategy to the given value
    def set_elevation_strategy(self, elevation_strategy):
        self._elevation_strategy = elevation_strategy

    # return elevation strategy
    def get_elevation_strategy(self):
        return self._elevation_strategy
    
    # set the start pont to the given value
    def set_start_point(self, start_point):
        self.start_point = start_point

    # set end point to the given value
    def set_end_point(self, end_point):
        self.end_point = end_point

    # If weight type is NORMAL return the length attribute of the edge; 
    # if the length attribute doesnt exist return weight attribute
    # and if the weight type is ElevationGain, return the difference in 
    # elevation b/n the two nodes.

    def get_weight(self, graph, node_1, node_2, weight_type=ElevationGain.NORMAL.value):
        if weight_type == ElevationGain.NORMAL.value:
            try:
                return graph.edges[node_1, node_2, 0][LENGTH]
            except:
                return graph.edges[node_1, node_2][WEIGHT]
        elif weight_type == ElevationGain.ELEVATION_GAIN.value:
            return max(0.0, graph.nodes[node_2][ELEVATION] - graph.nodes[node_1][ELEVATION])
        
    # By iterating over each pair of nodes in the route and adding 
    # the weight of the edge between them, 
    # this method determines the total weight of a particular 
    # route and returns the resulting total weight.
    def get_path_weight(self, graph, route, weight_attribute):
        total = 0
        for i in range(len(route) - 1):
            total += self.get_weight(graph, route[i], route[i + 1], weight_attribute)
        return total