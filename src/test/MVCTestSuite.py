import unittest
import networkx as nx
import sys
sys.path.append("../../")
from  src.Model.MapGraphModel import MapGraphModel
import googlemaps
from src.webapp import *
from geopy.geocoders import Nominatim
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.MapGraphModel import MapGraphModel
from Controller import AStarController, ShortestPathController, DijsktraController
from src.View.MapView import MapView
import warnings
import os

# Filter out the specific warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

class MVCTestSuite(unittest.TestCase):
    """
    This is the test suite for Model View Controller framework.
    """

    def test_dijkstra_parameters_max(self):
        """
        Test Dijkstra Algorithm with maximum elevation strategy and validate the parameters
        """
        # Define destination and origin address
        destination = "Brandywine Apartments, Brandywine, Amherst, MA, USA"
        origin = "Boulders Drive, Amherst, MA, USA"

        # get the latitude and logitude coordinates for the origin and the destination
        geocode_result = gmaps.geocode(origin)
        origin_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        geocode_result = gmaps.geocode(destination)
        destination_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        path_limit = 100
        elevation_strategy = "max"

        # Create instances of the required controllers and models
        controller = DijsktraController.DijsktraController()
        shortest_route_controller = ShortestPathController.ShortestPathController()

        model = AlgorithmModel()
        
        graphModel = MapGraphModel()
        # set the graph and other parameters for the controllers and models
        model.set_graph(graphModel.get_map_graph(destination_location))
        shortest_route_controller.G = graphModel.G
        shortest_path = shortest_route_controller.get_shortest_path(origin_location, destination_location)
        view = MapView()
        controller.set_contents(model.get_graph(), shortest_path.get_origin(), shortest_path.get_destination(), path_limit, 100, 
                                elevation_strategy, shortest_path)
        controller.set_model(model)
        elevation_path = controller.fetch_route_with_elevation()
        # register the views and update the state
        shortest_path.register(view)
        shortest_path.state_changed()
        elevation_path.register(view)
        elevation_path.state_changed()
        # validate the parameter and results
        _, elevation_gain, _  = view.get_route_params()
        assert model.get_elevation_strategy() == "max"
        assert controller.model.get_elevation_strategy() == "max"
        assert controller.get_elevation_strategy() == "max"
        assert controller.get_algo() == "Dijkstra Algorithm."
        assert elevation_path.get_algo() == "Dijkstra Algorithm."
        assert elevation_gain == elevation_path.get_gain()
    
    def test_dijkstra_parameters_min(self):
        """
        Test the Dijkstra algorithm with the minimum elevation strategy and  validate the parameters
        """
        # Define destination and origin address
        destination = "Brandywine Apartments, Brandywine, Amherst, MA, USA"
        origin = "Boulders Drive, Amherst, MA, USA"
        # get the latitude and logitude coordinates for the origin and the destination
        geocode_result = gmaps.geocode(origin)
        origin_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        geocode_result = gmaps.geocode(destination)
        destination_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        path_limit = 100
        elevation_strategy = "min"

        # Create instances of the required controllers and models
        controller = DijsktraController.DijsktraController()
        shortest_route_controller = ShortestPathController.ShortestPathController()

        model = AlgorithmModel()
        
        graphModel = MapGraphModel()
        # set the graph and other parameters for the controllers and models
        model.set_graph(graphModel.get_map_graph(destination_location))
        shortest_route_controller.G = graphModel.G
        shortest_path = shortest_route_controller.get_shortest_path(origin_location, destination_location)
        view = MapView()
        controller.set_contents(model.get_graph(), shortest_path.get_origin(), shortest_path.get_destination(), path_limit, 100, 
                                elevation_strategy, shortest_path)
        controller.set_model(model)
        elevation_path = controller.fetch_route_with_elevation()
        # register the views and update the state
        shortest_path.register(view)
        shortest_path.state_changed()
        elevation_path.register(view)
        elevation_path.state_changed()
        # validate the parameter and results
        _, elevation_gain, _  = view.get_route_params()
        assert model.get_elevation_strategy() == "min"
        assert controller.model.get_elevation_strategy() == "min"
        assert controller.get_elevation_strategy() == "min"
        assert controller.get_algo() == "Dijkstra Algorithm."
        assert elevation_path.get_algo() == "Dijkstra Algorithm."
        assert elevation_gain == elevation_path.get_gain()

    def test_astar_path_max(self):
        """
        Test A* algorithm with maximun elevation strategy and validate the parameters
        """
        # Define destination and origin address
        destination = "Brandywine Apartments, Brandywine, Amherst, MA, USA"
        origin = "Boulders Drive, Amherst, MA, USA"
        # get the latitude and logitude coordinates for the origin and the destination
        geocode_result = gmaps.geocode(origin)
        origin_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        geocode_result = gmaps.geocode(destination)
        destination_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        path_limit = 100
        elevation_strategy = "max"

        # Create instances of the required controllers and models
        controller = AStarController.AStarController()
        shortest_route_controller = ShortestPathController.ShortestPathController()
        model = AlgorithmModel()
        graphModel = MapGraphModel()
        # set the graph and other parameters for the controllers and models
        model.set_graph(graphModel.get_map_graph(destination_location))
        shortest_route_controller.G = graphModel.G
        shortest_path = shortest_route_controller.get_shortest_path(origin_location, destination_location)
        view = MapView()
        controller.set_contents(model.get_graph(), shortest_path.get_origin(), shortest_path.get_destination(), None, path_limit, 100, 
                                elevation_strategy, shortest_path)
        controller.set_model(model)
        elevation_path = controller.fetch_route_with_elevation()
        # register the views and update the state
        shortest_path.register(view)
        shortest_path.state_changed()
        elevation_path.register(view)
        elevation_path.state_changed()
        # validate the parameter and results
        _, elevation_gain , _ = view.get_route_params()
        assert controller.model.get_elevation_strategy() == "max"
        assert controller.get_elevation_strategy() == "max"
        assert controller.get_algo() == "A* Algorithm."
        assert elevation_path.get_algo() == "A* Algorithm."
        assert elevation_gain == elevation_path.get_gain()
        assert model.get_elevation_strategy() == "max"

    def test_astar_path_min(self):
        """
        Test A* algorithm with minimum elevation strategy and validate the parameters
        """
        # Define destination and origin address
        destination = "Brandywine Apartments, Brandywine, Amherst, MA, USA"
        origin = "Boulders Drive, Amherst, MA, USA"
        # get the latitude and logitude coordinates for the origin and the destination
        geocode_result = gmaps.geocode(origin)
        origin_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        geocode_result = gmaps.geocode(destination)
        destination_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        path_limit = 100
        elevation_strategy = "min"

        # Create instances of the required controllers and models
        controller = AStarController.AStarController()
        shortest_route_controller = ShortestPathController.ShortestPathController()
        model = AlgorithmModel()
        graphModel = MapGraphModel()
        # set the graph and other parameters for the controllers and models
        model.set_graph(graphModel.get_map_graph(destination_location))
        shortest_route_controller.G = graphModel.G
        shortest_path = shortest_route_controller.get_shortest_path(origin_location, destination_location)
        view = MapView()
        controller.set_contents(model.get_graph(), shortest_path.get_origin(), shortest_path.get_destination(), None, path_limit, 100, 
                                elevation_strategy, shortest_path)
        controller.set_model(model)
        elevation_path = controller.fetch_route_with_elevation()
        # register the views and update the state
        shortest_path.register(view)
        shortest_path.state_changed()
        elevation_path.register(view)
        elevation_path.state_changed()
        # validate the parameter and results
        _, elevation_gain , _ = view.get_route_params()
        assert controller.model.get_elevation_strategy() == "min"
        assert controller.get_elevation_strategy() == "min"
        assert controller.get_algo() == "A* Algorithm."
        assert elevation_path.get_algo() == "A* Algorithm."
        assert elevation_gain == elevation_path.get_gain()
        assert model.get_elevation_strategy() == "min"
        

if __name__ == '__main__':
    os.chdir("../../")
    unittest.main()