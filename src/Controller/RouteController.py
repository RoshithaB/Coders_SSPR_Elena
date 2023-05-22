
from . import ShortestPathController
from . import AStarController
from . import DijsktraController
from src.utils import ElevationStrategy, RouteAlgorithms

from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.MapGraphModel import MapGraphModel

class RouteController:
    def __init__(self):
        """
        This method initializes the  route and algorithm attributes
        """
        self.algorithm_model = AlgorithmModel()
        self.shortest_path = None
        self.elevation_path = None
        self.algo = RouteAlgorithms.ASTAR_ALGORITHM.value

    def get_algo(self, algo):
        return self.algo

    def set_algo(self, algo):
        self.algo = algo

    def calcuate_elevation_astar_path(self):
        """
        This method sets the shortest path based on the starting and ending coordinates.

        Args:
            origin:
            dest:

        Returns:
            Shortest Path model
        """
        astar_controller = AStarController.AStarController()

        graph = self.algorithm_model.get_graph()
        origin = self.shortest_path.get_origin()
        destination = self.shortest_path.get_destination()
        path_limit = self.algorithm_model.get_path_limit()
        elevation_strategy =  self.algorithm_model.get_elevation_strategy()
        shortest_path = self.shortest_path

        astar_controller.set_contents(graph, origin, destination, None, path_limit, 100, elevation_strategy, shortest_path)
        return astar_controller.fetch_route_with_elevation()
    
    def calcuate_elevation_dijkstra_path(self):
        dijkstra_controller = DijsktraController.DijsktraController()

        graph = self.algorithm_model.get_graph()
        origin = self.shortest_path.get_origin()
        destination = self.shortest_path.get_destination()
        path_limit = self.algorithm_model.get_path_limit()
        elevation_strategy =  self.algorithm_model.get_elevation_strategy()
        shortest_path = self.shortest_path

        dijkstra_controller.set_contents(graph, origin, destination, path_limit, 100, elevation_strategy, shortest_path)
        return dijkstra_controller.fetch_route_with_elevation()

    def calculate_shortest_path(self, origin, dest):
        """
        This method sets the shortest path based on the starting and ending coordinates.

        Args:
            origin:
            dest:

        Returns:
            Shortest Path model
        """
        self.algorithm_model.set_graph(MapGraphModel().get_map_graph(dest))
        controller = ShortestPathController.ShortestPathController()
        controller.set_graph(self.algorithm_model.get_graph())
        return controller.get_shortest_path(origin, dest)


    def calculate_final_route(self, start, end, elev_gain, map_view, dev_percent):
        """
        This method gets the final shortest path calculated on the elevation strategy and the path limit specified.
        Args:
            start:
            end:
            elev_gain:
            map_view:
            dev_percent:
        """
        # Shortest path calculation
        self.shortest_path = self.calculate_shortest_path(start, end)

        total_dist = str(self.shortest_path.get_distance())
        elevation_gain = str(self.shortest_path.get_gain())
        algo = self.shortest_path.get_algo()
        print("Total Distance: " + total_dist)
        print("Elevation Gain: " + elevation_gain)
        print("Implemented Algorithm: " + algo)

        if dev_percent == "100":
            self.shortest_path.register(map_view)
            self.shortest_path.state_changed()
            return
        

        # Elevated path calculation
        self.algorithm_model.set_path_limit(float(dev_percent) / 100.0)
        self.algorithm_model.set_elevation_strategy(elev_gain)

        if self.algo == RouteAlgorithms.DIJKSTRA_ALGORITHM.value:
            self.elevation_path = self.calcuate_elevation_dijkstra_path()
        else:
            self.elevation_path = self.calcuate_elevation_astar_path()
        print("Total Distance: " + str(self.elevation_path.get_distance()))
        print("Elevation Gain: " + str(self.elevation_path.get_gain()))
        print("Implemented Algorithm: " + self.elevation_path.get_algo())

        self.shortest_path.register(map_view)
        self.shortest_path.state_changed()
        self.elevation_path.register(map_view)
        self.elevation_path.state_changed()