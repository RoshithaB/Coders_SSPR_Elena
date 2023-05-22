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

    def test_dijkstra_parameters(self):
        destination = "Brandywine Apartments, Brandywine, Amherst, MA, USA"
        origin = "Boulders Drive, Amherst, MA, USA"
        geocode_result = gmaps.geocode(origin)
        origin_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        geocode_result = gmaps.geocode(destination)
        destination_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        path_limit = 100
        elevation_strategy = "max"

        controller = DijsktraController.DijsktraController()
        shortest_route_controller = ShortestPathController.ShortestPathController()

        model = AlgorithmModel()
        
        graphModel = MapGraphModel()
        model.set_graph(graphModel.get_map_graph(destination_location))
        shortest_route_controller.G = graphModel.G
        shortest_path = shortest_route_controller.get_shortest_path(origin_location, destination_location)
        view = MapView()
        controller.set_contents(model.get_graph(), shortest_path.get_origin(), shortest_path.get_destination(), path_limit, 100, 
                                elevation_strategy, shortest_path)
        elevation_path = controller.fetch_route_with_elevation()
        shortest_path.register(view)
        shortest_path.state_changed()
        elevation_path.register(view)
        elevation_path.state_changed()
        #print(controller.get_elevation_strategy())
        #print(controller.get_algo())
        #print(elevation_path.get_algo())
        _, elevation_gain, _  = view.get_route_params()
        #print(elevation_gain)
        print(model.get_elevation_strategy())
        assert controller.get_elevation_strategy() == "max"
        # assert controller.get_algo() == "Dijkstra Algorithm."
        assert elevation_path.get_algo() == "Dijkstra Algorithm."
        assert elevation_gain == elevation_path.get_gain()
        #assert model.get_elevation_strategy() == "max"

    def test_astar_path_min(self):
        destination = "Brandywine Apartments, Brandywine, Amherst, MA, USA"
        origin = "Boulders Drive, Amherst, MA, USA"
        geocode_result = gmaps.geocode(origin)
        origin_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        geocode_result = gmaps.geocode(destination)
        destination_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        path_limit = 100
        elevation_strategy = "min"

        controller = AStarController.AStarController()
        shortest_route_controller = ShortestPathController.ShortestPathController()
        #os.chdir("../../")
        model = AlgorithmModel()
        graphModel = MapGraphModel()
        model.set_graph(graphModel.get_map_graph(destination_location))
        shortest_route_controller.G = graphModel.G
        shortest_path = shortest_route_controller.get_shortest_path(origin_location, destination_location)
        view = MapView()
        controller.set_contents(model.get_graph(), shortest_path.get_origin(), shortest_path.get_destination(), None, path_limit, 100, 
                                elevation_strategy, shortest_path)
        elevation_path = controller.fetch_route_with_elevation()
        shortest_path.register(view)
        shortest_path.state_changed()
        elevation_path.register(view)
        elevation_path.state_changed()
        _, elevation_gain , _ = view.get_route_params()
        print(model.get_elevation_strategy())
        assert controller.get_elevation_strategy() == "min"
        # assert controller.get_algo() == "Dijkstra Algorithm."
        assert elevation_path.get_algo() == "A* Algorithm."
        assert elevation_gain == elevation_path.get_gain()
        #assert model.get_elevation_strategy() == "min"
        

if __name__ == '__main__':
    os.chdir("../../")
    unittest.main()