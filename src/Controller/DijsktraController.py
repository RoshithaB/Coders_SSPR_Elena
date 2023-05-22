import math
import osmnx  as ox
from src.Model.AlgorithmModel import AlgorithmModel
from src.Model.PathModel import *
from . import AbstractAlgorithm
import networkx as nx
from src.utils import calculate_astar_path, ElevationGain, ElevationStrategy
from src.utils import Constants, RouteAlgorithms

#class DijsktraController(AbstractAlgorithm.AbstractAlgorithm):
