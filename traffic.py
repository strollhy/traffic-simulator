__author__ = 'hongyusong'


class Car():
    def __init__(self, **kwargs):
        self.car_id = 0
        self.path = None        # Path
        self.distance = 0
        self.location = None    # Link
        self.speed = 0
        self.start_time = 0
        self.arrive_time = []   # list of int

######################################################


class Link():
    def __init__(self, **kwargs):
        self.road_id = 0
        self.length = 0
        self.num_of_cars = 0
        self.head_node = None       # Node
        self.tail_node = None       # Node
        self.capacity = 0
        self.speed_limit = [0, 0]   # tuple
        self.avg_speed = 0
        self.avg_density = 0
        self.next_links = {}        # {'l': Link, 'r': Link, 'u': Link}
        self.time_stamp = 0         # might not be used


class SubLink1(Link):
    def __init__(self, link):
        self.parent_link = link


class SubLink2(Link):
    def __init__(self, link):
        self.parent_link = link


class SubLink3(Link):
    def __init__(self, link):
        self.parent_link = link


class Path():
    def __init__(self, **kwargs):
        self.links = ()
        self.od = (0, 0)

######################################################


class Node():
    def __init__(self, links, lights):
        self.links = links          # list of Link
        self.lights = lights        # list of light

    def update_light(self, lights):
        self.lights = lights