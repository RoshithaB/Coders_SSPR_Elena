
from . import ShortestPathController
from . import AlgorithmController
from . import AStarController

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

    def calcuate_elevation_path(self):
        """
        This method sets the shortest path based on the starting and ending coordinates.

        Args:
            origin:
            dest:

        Returns:
            Shortest Path model
        """
        astar_controller = AStarController.AStarController()
        print(self.algorithm_model.get_elevation_strategy())
        astar_controller.set_contents(self.algorithm_model.get_graph(), 
                                    self.shortest_path.get_origin(),
                                    self.shortest_path.get_destination(),
                                    None,
                                    self.algorithm_model.get_path_limit(),
                                    100,
                                    self.algorithm_model.get_elevation_strategy(),
                                    self.shortest_path
                                    )
        """
        algorithm_controller = AlgorithmController(self.algorithm_model.get_graph(),
                                    self.shortest_path.get_distance(),
                                    self.algorithm_model.get_path_limit(),
                                    self.algorithm_model.get_elevation_strategy(),
                                    self.shortest_path.get_origin(),
                                    self.shortest_path.get_destination(),
                                    self.shortest_path.get_gain(),
                                    self.algorithm_model.get_algo_flag())
        """
        return astar_controller.fetch_route_with_elevation()

    def print_route_attributes(self, path):
        """
        This method displays the path information.
        Args:
            path:

        Returns:

        """
        print("Total Distance: " + str(path.get_distance()))
        print("Elevation Gain: " + str(path.get_gain()))
        print("Implemented Algorithm: " + path.get_algo())

    def calculate_final_route(self, start_point, end_point, deviation_percent, minmax_elev_gain, map_view):
        """
        This method gets the final shortest path calculated on the elevation strategy and the path limit specified.
        Args:
            start_point:
            end_point:
            deviation_percent:
            minmax_elev_gain:
            algo:
            map_view:
        """
        # Shortest path calculation
        #print(start_point)
        #print(end_point)
        self.shortest_path = self.calculate_shortest_path(start_point, end_point)
        self.print_route_attributes(self.shortest_path)

        if deviation_percent == "100":
            self.shortest_path.register(map_view)
            self.shortest_path.state_changed()
            return

        # Elevated path calculation
        self.algorithm_model.set_path_limit(float(deviation_percent) / 100.0)
        self.algorithm_model.set_elevation_strategy(minmax_elev_gain)
        self.algorithm_model.set_algo_flag(2)

        self.elevation_path = self.calcuate_elevation_path()
        self.print_route_attributes(self.elevation_path)

        self.shortest_path.register(map_view)
        self.shortest_path.state_changed()
        self.elevation_path.register(map_view)
        self.elevation_path.state_changed()