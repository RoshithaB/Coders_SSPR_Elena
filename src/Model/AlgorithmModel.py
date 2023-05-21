from src.utils import ElevationGain

LENGTH = "length"
WEIGHT = "weight"
ELEVATION = "elevation"


class AlgorithmModel:
    """
    This class initializes critical parameters such the graph,the algorithm,the path_limit  etc.It contains methods to register the
    observer,set the algorithm,set the algorithm object,print the route information etc and also it notifies the observers.
    """

    def __init__(self):
        """
        This method initializes the  route and algorithm attributes
        """
        self._graph = None
        self._observer = None
        self._algorithm = None
        self._path_limit = None
        self._elevation_strategy = None
        self._algo_flag = 1
        self._heuristic = None

    def set_graph(self, graph):
        self.graph = graph
    
    def get_graph(self):
        return self.graph
    
    def set_algo_flag(self, algo_flag):
        self.algo_flag = algo_flag
    
    def get_algo_flag(self):
        return self.algo_flag

    def set_path_limit(self, path_limit):
        self.path_limit = path_limit
    
    def get_path_limit(self):
        return self.path_limit

    def set_elevation_strategy(self, elevation_strategy):
        self.elevation_strategy = elevation_strategy
    
    def get_elevation_strategy(self):
        return self.elevation_strategy

    def set_start_point(self, start_point):
        self.start_point = start_point

    def set_end_point(self, end_point):
        self.end_point = end_point

    def get_weight(self, graph, node_1, node_2, weight_type=ElevationGain.NORMAL.value):
        if weight_type == ElevationGain.NORMAL.value:
            try:
                return graph.edges[node_1, node_2, 0][LENGTH]
            except:
                return graph.edges[node_1, node_2][WEIGHT]
        elif weight_type == ElevationGain.ELEVATION_GAIN.value:
            return max(0.0, graph.nodes[node_2][ELEVATION] - graph.nodes[node_1][ELEVATION])

    def get_path_weight(self, graph, route, weight_attribute):
        total = 0
        for i in range(len(route) - 1):
            total += self.get_weight(graph, route[i], route[i + 1], weight_attribute)
        return total