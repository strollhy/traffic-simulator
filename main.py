__author__ = 'hongyusong'

from traffic import *
from link import *
from rule import Rule

######################################################
# car_data = [["1", "1,2,3", "0"],
#             ["2", "2,3", "1"],
#             ["3", "1,2", "2"],
#             ["4", "1,2,3", "1"],
#             ["5", "1,2,3", "2"],
#             ["6", "1,2,3", "3"],
#             ["7", "2,3", "2"],
#             ["8", "1,2,3", "3"],
#             ["9", "1,2,3", "3"],
#             ["10", "1,2,3", "3"],
#             ["11", "1,2,3", "3"],
#             ]
# link_data = [["1000", "4", "20", "50", "220", "4", "5", "5"],
#              ["800", "4", "20", "50", "220", "4", "5", "5"],
#              ["900", "4", "20", "50", "220", "4", "5", "5"]]
# link_link_data = [["1", "2", "0", "0"],
#                   ["2", "0", "0", "3"],
#                   ["3", "0", "0", "0"]]
# light_data = [["1", "2,3", "2,3", "2,3"],
#               ["2", "2,3", "3,4", "5,1"],
#               ["3", "2,3", "4,3", "1,5"]]

######################################################


class Simulator:
    def __init__(self):
        self.time = 0
        self.total_time = 0
        self.cars = {}
        self.links = {}
        self.setup_links()
        self.setup_cars()
        self.setup_lights()
        self.rule = Rule(self)

    def start(self):
        while self.total_time > self.time:
            self.next_time_stamp()

    def next_time_stamp(self):
        self.print_status()
        self.update_time()
        self.update_cars()
        self.update_links()
        self.time += 1

    def setup_cars(self):
        # Setup cars
        f = open('data/car.csv')
        f.readline()
        for line in f:
            data = line.strip().split(',')
            car = Car(*data)
            car.get_directions(self.get_directions)
            self.cars[data[0]] = car
            self.links[car.path[0]].sublink1.add_car(car)

    def setup_links(self):
        # Setup links
        f = open('data/link.csv')
        f.readline()
        for line in f:
            link_data = line.strip().split(',')
            link_id = link_data[0]
            self.links[link_id] = MainLink(*link_data)

        # Setup link connections
        f = open('data/link2link.csv')
        f.readline()
        for line in f:
            link_link_data = line.strip().split(',')
            link_id = link_link_data[0]

            if link_link_data[1] != '0':
                self.links[link_id].left_link = self.links[link_link_data[1]]
                self.links[link_link_data[1]].right_link = self.links[link_id]
            if link_link_data[2] != '0':
                self.links[link_id].right_link = self.links[link_link_data[2]]
                self.links[link_link_data[2]].left_link = self.links[link_id]
            if link_link_data[3] != '0':
                self.links[link_id].through_link = self.links[link_link_data[3]]
                self.links[link_link_data[3]].through_link = self.links[link_id]

    def setup_lights(self):
        # Setup nodes
        f = open('data/signal.csv')
        f.readline()
        for line in f:
            data = line.strip().split(',')
            link_id = data[0]
            direction = data[1]
            if direction in ["T", "R", "L"]:
                self.links[link_id].sublink3.setup_signal(direction, data[2:])
        self.update_time()
        self.total_time = len(data[2:])

    def get_directions(self, link_id, next_link_id):
        link = self.links[link_id]
        if link.left_link and link.left_link.link_id == next_link_id:
            return "L"
        if link.right_link and link.right_link.link_id == next_link_id:
            return "R"
        if link.through_link and link.through_link.link_id == next_link_id:
            return "T"

    def update_time(self):
        for link in self.links.values():
            link.sublink3.update_time(self.time)

    def update_cars(self):
        self.rule.update_cars()

    def update_links(self):
        self.rule.update_links()

    # outputs
    def print_status(self):
        print "==== Time Stamp %ds =====" % (self.time * 10)
        # for link_id in sorted(self.links.keys()):
        #     link = self.links[link_id]
        #     link.sublink3.print_lights()


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()