import osmnx as ox
import os
import pickle as pkl
import numpy as np
from src.utils import Constants
import sys


class MapGraphModel:
    """
    Graph making techniques for a selected destination are provided by this class.
    """
    def __init__(self):
        self.G= None
        self.initial_point = (42.3867637, -72.5322402) # Co-ordinates of UMass Amherst
        self.saved_map_path = "src/graph.p"
        self.saved_map_path = os.path.abspath(self.saved_map_path)
        self.gmap_api_key = Constants.GOOGLEMAPS_CLIENT_KEY.value
        self.isMapLoaded = os.path.exists(self.saved_map_path)
    
    """
    Given latitudes and longitudes of two nodes, returns the distance between them.
    """ 
    def dist_nodes(self,lat1,long1,lat2,long2):
		
        radius=6371008.8 
        
        lat1, long1 = np.radians(lat1), np.radians(long1)
        lat2, long2 = np.radians(lat2),np.radians(long2)

        dlong,dlat = long2 - long1,lat2 - lat1

        temp1 = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlong / 2)**2
        temp2 = 2 * np.arctan2(np.sqrt(temp1), np.sqrt(1 - temp1))
        return radius * temp2

    """
    This is the method for adding the graph's nodes' distances from the destination node.
    """
    def find_dist_to_destination(self, dest_node):
       
        end_node = self.G.nodes[ox.get_nearest_node(self.G, point=dest_node)]
        for node, data in self.G.nodes(data=True):
            node_lat = self.G.nodes[node]['x']
            node_long = self.G.nodes[node]['y']
            last_lat = end_node['x']
            last_long = end_node['y']
            data['dist_from_dest'] = self.dist_nodes(last_lat,last_long,node_lat,node_long)
        return self.G
    
    """
    This is the method for returning a graph with edge grades and elevation 
    information added to the graph nodes.
    """
    def get_map_graph(self, dest_node):
        
        if not self.isMapLoaded:
            print("Fetching the Map")
            self.G = ox.graph_from_point(self.initial_point, dist=20000, network_type='walk')

            # appending elevation data to each node and populating the graph
            self.G = ox.add_node_elevations(self.G, api_key=self.gmap_api_key) 
            pkl.dump(self.G, open(self.saved_map_path, "wb"))
            print("Stored the Map")
        else:
            with open(self.saved_map_path, "rb") as file:
                self.G = pkl.load(file)
                self.G = ox.add_edge_grades(self.G)
        return self.find_dist_to_destination(dest_node)
