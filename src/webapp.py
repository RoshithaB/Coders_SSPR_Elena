from src.View.MapView import MapView
from . import app
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import googlemaps
import sys
sys.path.append("..")
from src.Controller.RouteController import RouteController
from src.utils import Constants, RouteAlgorithms
import json

gmaps = googlemaps.Client(key=Constants.GOOGLEMAPS_CLIENT_KEY.value)

@app.route("/")
def home():
	"""
	Route handler for the home page
	"""
	return render_template("index.html")

@app.route('/<request>', methods=['GET'])
def go(request):
	"""
	Route handler for processing the request and generating the route
	"""
	if bool(request):

		request = request.replace("%2C", "," ).replace("%20", " " )
		start_loc, end_loc, percentage, minmax_elev_gain, algo = request.split(":")
		
		print("\n-------------------------------\nInput Parameters\n")
		print(start_loc)
		print(end_loc)
		print(percentage)
		print(minmax_elev_gain)
		print(algo)
		print("-------------------------------\n")

		start_lat = gmaps.geocode(start_loc)[0]['geometry']['location']['lat']
		start_long = gmaps.geocode(start_loc)[0]['geometry']['location']['lng']
		end_lat = gmaps.geocode(end_loc)[0]['geometry']['location']['lat']
		end_long = gmaps.geocode(end_loc)[0]['geometry']['location']['lng']
		start_coord = [start_lat, start_long]
		end_coord = [end_lat, end_long]

		view = MapView()

		controller = RouteController()
		if algo == 'a-star':
			controller.set_algo(RouteAlgorithms.ASTAR_ALGORITHM.value)
		else:
			controller.set_algo(RouteAlgorithms.DIJKSTRA_ALGORITHM.value)

		controller.calculate_final_route(start_coord, end_coord, minmax_elev_gain, view, percentage)
		path_coord, elev, total_dist = view.get_route_params()
		tmp_path_coord = []
		for coord in path_coord:
			tmp_path_coord.append(coord[::-1])
		path_coord = tmp_path_coord

		path = [[]]
		c = 0
		print("\n-------------------------------\nPath Coordinates:\n")
		print(len(path_coord), path_coord)
		
		for coord in path_coord:
			if c == 23:
				c = 0
				path.append([])
			path[-1].append(coord)
			c += 1
		print("-------------------------------\n")
		print("Elevation:", elev)
	return jsonify(origin=start_coord, des=end_coord,path=path, dis=total_dist, elev=elev)