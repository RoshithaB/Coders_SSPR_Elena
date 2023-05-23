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

class AlgorithmTestSuite(unittest.TestCase):
    """
    This test suite includes unit test cases for inspecting the graph using smaller and visualizer-friendly graphs.
    Additionally, the algorithms Dijkstra and A* are examined and compared using different extra path limit values.
    """
    G = None

    @classmethod
    def setUpClass(self):
        """
        This is the setup method that is called before the test cases are executed once
       
        """
        # Creating a test graph.
        G = nx.Graph()
        # Adding the a few nodes
        [G.add_node(i, elevation=0.0) for i in range(5)]
        # Adding edge lengths
        edge_lengths = [(0, 1, 5), (1, 2, 8.5), (1, 3, 8), (3, 4, 7), (4, 2, 10), (1, 4, 3)]
        # Adding edge elevations
        edge_elevations = [(0, 1, 5.0), (1, 2, 2.0), (1, 3, 1.0), (3, 4, -4.0), (4, 2, -3.0), (1, 4, 4.0)]
        edge_abs_elevations = [(0, 1, 5.0), (1, 2, 2.0), (1, 3, 1.0), (3, 4, 4.0), (4, 2, 3.0), (1, 4, 4.0)]
        G.add_weighted_edges_from(edge_lengths)
        G.add_weighted_edges_from(edge_elevations, weight="grade")
        G.add_weighted_edges_from(edge_abs_elevations, weight="grade_abs")
        elev = [0.0, 0.0, 1.0, 3.0, 4.0]
        for i, e in enumerate(elev):
            G.nodes[i]["elevation"] = e
        self.G = G

    def test_conversions(self):
        """
        The purpose of this test is to evaluate how well coordinates and location can be converted 
        """
        main_address = "13 Brandywine Drive, Amherst, Massachusetts, United States"
        geocode_result = gmaps.geocode(main_address)
        (x, y) = (geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng'])
        assert isinstance(x, float)
        assert isinstance(y, float)
        # Create a geocoder instance
        geolocator = Nominatim(user_agent="myGeocoder")
        # Reverse geocode the location
        address = geolocator.reverse((x,y))
        # Extract the desired components from the address
        short_address = f"{address.raw['address']['house_number']} {address.raw['address']['road']}, {address.raw['address']['town']}, {address.raw['address']['state']}, {address.raw['address']['country']}"
        assert short_address == main_address

    def test_weights_functions(self):
        """
        This testcase is to check if the weights are computed properly

        """
        route = [0, 1, 2, 4]
        am_instance = AlgorithmModel()
        weight = am_instance.get_path_weight(self.G, route, "normal")
        assert weight == 23.5

    def test_astar_path_max(self):
        """
        Test the A* algorithm with the maximum elevation strategy
        """
        destination = "Brandywine Apartments, Brandywine, Amherst, MA, USA"
        origin = "Boulders Drive, Amherst, MA, USA"
        geocode_result = gmaps.geocode(origin)
        origin_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        geocode_result = gmaps.geocode(destination)
        destination_location = [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
        path_limit = 100
        elevation_strategy = "max"

        controller = AStarController.AStarController()
        shortest_route_controller = ShortestPathController.ShortestPathController()

        model = AlgorithmModel()
        os.chdir("../../")
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
        _, _, shortest_distance = view.get_route_params()
        elevation_path.register(view)
        elevation_path.state_changed()
        _, _, astar_distance = view.get_route_params()
        assert astar_distance >= shortest_distance, "Elevation distance \
                                    should always be greater than or equal to the shortest distance."
        
        # assert elevation as well

    def test_astar_path_min(self):
        """
        Test the A* algorithm with the minimum elevation strategy
        """
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
        _, _, shortest_distance, = view.get_route_params()
        elevation_path.register(view)
        elevation_path.state_changed()
        _, _,  astar_distance = view.get_route_params()
        assert astar_distance >= shortest_distance, "Elevation distance \
                                    should always be greater than or equal to the shortest distance."
        
    def test_dijsktra_path_max(self):
        """
        Test the Dijkstra Algorithm with the maximum elevation strategy
        """
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
        _, _, shortest_distance = view.get_route_params()
        elevation_path.register(view)
        elevation_path.state_changed()
        _, _, astar_distance = view.get_route_params()
        assert astar_distance >= shortest_distance, "Elevation distance \
                                    should always be greater than or equal to the shortest distance."
        
    def test_dijsktra_path_min(self):
        """
        Test the Dijkstra Algorithm with the minimum elevation strategy
        """
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
        _, _, shortest_distance = view.get_route_params()
        elevation_path.register(view)
        elevation_path.state_changed()
        _, _, astar_distance = view.get_route_params()
        assert astar_distance >= shortest_distance, "Elevation distance \
                                    should always be greater than or equal to the shortest distance."
    


if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(AlgorithmTestSuite)

    # Create a test runner
    test_runner = unittest.TextTestRunner(verbosity=1)  # Set verbosity=2 for verbose output

    # Run the tests
    test_runner.run(test_suite)