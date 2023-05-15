import osmnx as ox
#from haversine import haversine, Unit
# import haversine
import os
import pickle as pkl
import numpy as np

class MapGraphModel:
    """
    Class providing the methods to create a graph with elevation details for a selected destination.
    """
    def __init__(self):
        self.G= None
        self.initial_point = (42.3867637, -72.5322402) # Co-ordinates of UMass Amherst
        self.saved_map_path = "src/graph.p"
        self.gmap_api_key = "AIzaSyAwgA49m7P_jYVRdLY2aS8uy7VIGYkpweE"
        self.isMapLoaded = os.path.exists(self.saved_map_path)
    
    def dist_nodes(self,lat1,long1,lat2,long2):
		# Given latitudes and longitudes of two nodes, returns the distance between them.
        radius=6371008.8 # Earth radius
        
        lat1, long1 = np.radians(lat1), np.radians(long1)
        lat2, long2 = np.radians(lat2),np.radians(long2)

        dlong,dlat = long2 - long1,lat2 - lat1

        temp1 = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlong / 2)**2
        temp2 = 2 * np.arctan2(np.sqrt(temp1), np.sqrt(1 - temp1))
        return radius * temp2

    def find_dist_to_destination(self, dest_node):
        """
        Method to add distances from dest node to all nodes in the graph.
        """
        end_node = self.G.nodes[ox.get_nearest_node(self.G, point=dest_node)]
        for node, data in self.G.nodes(data=True):
            node_lat = self.G.nodes[node]['x']
            node_long = self.G.nodes[node]['y']
            last_lat = end_node['x']
            last_long = end_node['y']
            data['dist_from_dest'] = self.dist_nodes(last_lat,last_long,node_lat,node_long)
        return self.G

    def get_map_graph(self, dest_node):
        """
        Method to return graph with elevation details and edge grades added to the graph nodes.
        """
        if not self.isMapLoaded:
            print("Fetching the Map")
            self.G = ox.graph_from_point(self.initial_point, dist=20000, network_type='walk')

            # appending elevation data to each node and populating the graph
            self.G = ox.add_node_elevations(G, api_key=self.gmap_api_key) 
            pkl.dump(self.G, open(self.saved_map_path, "wb"))
            print("Stored the Map")
        else:
            self.G = pkl.load(open(self.saved_map_path, "rb"))
            self.G = ox.add_edge_grades(self.G)
        return self.find_dist_to_destination(dest_node)
