from flask import Flask, render_template, request, jsonify
from datetime import datetime

from src.View.Observer import Observer
from .. import app
import json
from src.utils import RouteAlgorithms

class MapView(Observer):
	"""
	A class representing a map view thats observes changes in path model.
	"""
	def __init__(self):
		super().__init__()
		self.route_coordinates = None
		self.total_distance = None
		self.elevation = None

	# Return the route parameters (route coordinates, elevation, total distance)
	def get_route_params(self):
		return (self.route_coordinates, self.elevation, self.total_distance)

	# Update the mapview with changes in path model
	def update(self, path_model):
		self.route_coordinates = path_model.get_path()
		self.total_distance = path_model.get_distance()

		if path_model.get_algo() == RouteAlgorithms.DIJKSTRA_ALGORITHM.value:
			self.elevation = path_model.get_gain()
		
		if path_model.get_algo() == RouteAlgorithms.ASTAR_ALGORITHM.value:
			self.elevation = path_model.get_gain()
		
        