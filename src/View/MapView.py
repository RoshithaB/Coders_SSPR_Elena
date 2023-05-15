from flask import Flask, render_template, request, jsonify
from datetime import datetime

from src.View.Observer import Observer
from .. import app
import json

class MapView(Observer):

	def __init__(self):
		super().__init__()
		self.route_coordinates = None
		self.total_distance = None
		self.elevation = None

	def update(self, path_model):
		self.route_coordinates = path_model.get_path()
		self.total_distance = path_model.get_distance()
		
		if path_model.get_path_flag() == 2:
			self.elevation = path_model.get_gain()

	def get_route_params(self):
		return (self.route_coordinates, self.total_distance, self.elevation)
        