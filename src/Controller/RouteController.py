
from . import ShortestPathController
from . import AStarController
from . import DijsktraController
from src.utils import ElevationStrategy, RouteAlgorithms

from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.MapGraphModel import MapGraphModel
import logging
import os

# Configure the logger
log_file = os.path.join("..", "logging.txt")
logging.basicConfig(filename=log_file, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RouteController:
    def __init__(self):
        """
         This technique sets the route and algorithm properties.
        """
        self.algorithm_model = AlgorithmModel()
        self.shortest_path = None
        self.elevation_path = None
        self.algo = RouteAlgorithms.ASTAR_ALGORITHM.value

    # returns the value of 'algo' attribute
    def get_algo(self, algo):
        return self.algo

    # sets the value of 'algo' attribute to the provided 'algo' value
    def set_algo(self, algo):
        logger.debug("Algorithm is set on  route controller.")
        self.algo = algo

    def calcuate_elevation_astar_path(self):
        """
        The starting and finishing coordinates are used to determine the shortest path.
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
        """
        Calculates the elevation-aware path using Dijkstra's algorithm 
        Returns:
            Shortest path model
        """
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
        The starting and finishing coordinates are used to determine the shortest path.

        Args:
            origin: the origin location co-ordinates
            dest: the destination location co-ordinates

        Returns:
            Shortest Path model
        """
        self.algorithm_model.set_graph(MapGraphModel().get_map_graph(dest))
        controller = ShortestPathController.ShortestPathController()
        controller.set_graph(self.algorithm_model.get_graph())
        return controller.get_shortest_path(origin, dest)


    def calculate_final_route(self, start, end, elev_gain, map_view, dev_percent):
        """
        Using the elevation strategy and supplied path limit, this method determines 
        the ultimate shortest path.
        Args:
            start: the origin location co-ordinates
            end: the destination location co-ordinates
            elev_gain: the input elevation gain
            map_view: the map-view being used to update the appropriate map
            dev_percent: max % of the shortest path
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