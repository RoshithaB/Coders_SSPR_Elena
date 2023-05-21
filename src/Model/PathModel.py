from src.Model.Observable import Observable
class PathModel(Observable):
    """
    Class that consists of getter and setter methods for path attributes.
    """
    def __init__(self):
        super().__init__()
        self.algo = ""
        self.gain = 0
        self.drop = 0
        self.path = []
        self.distance = 0.0
        self.origin = None, None
        self.destination = None, None
        self.path_flag = 1
        self.observers = set() #The set of observers that subscribe to be notified.
    
    """
        Register an observer
        @param obs = observer that needs to be registered
    """
    def register(self, obs):
        self.observers.add(obs)
    
    """
        Unregister a registered observer
        @param obs = observer that needs to be unregistered
    """
    def unegister(self, obs):
        self.observers.remove(obs)

    def set_algo(self, algo):
        self.algo = algo
        self.state_changed()

    def set_elevation_gain(self, gain):
        self.gain = gain
        self.state_changed()

    def set_drop(self, drop):
        self.drop = drop
        self.state_changed()

    def set_path(self, path):
        self.path = path
        self.state_changed()

    def set_distance(self, distance):
        self.distance = distance
        self.state_changed()
    
    def set_path_flag(self, path_flag):
        self.path_flag = path_flag
    
    def get_path_flag(self):
        return self.path_flag

    def get_algo(self):
        return self.algo

    def get_gain(self):
        return self.gain

    def get_drop(self):
        return self.drop

    def get_path(self):
        return self.path
    
    def get_distance(self):
        return self.distance

    def set_start_location(self, origin):
        self.origin = origin
        self.state_changed()

    def get_origin(self):
        return self.origin

    def set_end_location(self, destination):
        self.destination = destination
        self.state_changed()

    def get_destination(self):
        return self.destination
    
    def state_changed(self):
        for observer in self.observers:
            observer.update(self)
