__author__ = 'hongyusong'

from traffic import *
from rule import Rule

######################################################
car_data = [["1", "1,2", "0"],
            ["2", "2,3", "1"],
            ["3", "3,2", "10"]]
link_data = [["1000", "4", "20", "50", "220", "4", "5", "5"],
             ["800", "4", "20", "50", "220", "4", "5", "5"],
             ["900", "4", "20", "50", "220", "4", "5", "5"]]
link_link_data = [["1", "2", "0", "0"],
                  ["2", "0", "0", "3"],
                  ["3", "0", "0", "0"]]
light_data = [["1", "10,20", "10,20", "10,20"],
              ["2", "40,30", "50,50", "30,40"],
              ["3", "40,30", "50,50", "30,40"]]

######################################################


class Simulator:
    def __init__(self):
        self.time = 0
        self.cars = {}
        self.links = {}
        self.setup_cars()
        self.setup_links()
        self.setup_lights()
        self.rule = Rule(self)

    def start(self):
        for i in xrange(50):
            self.next_time_stamp()

    def next_time_stamp(self):
        self.update_lights()
        self.update_cars()
        self.update_links()
        self.time += 1

        self.print_status()

    def setup_cars(self):
        # Setup cars
        for data in car_data:
            self.cars[data[0]] = Car(data)

    def setup_links(self):
        # Setup links
        for i in xrange(len(link_data)):
            link_id = str(i + 1)
            self.links[link_id] = Link(link_id, *link_data[i])

        # Setup link connections
        for i in xrange(len(link_link_data)):
            data = link_link_data[i]
            link_id = str(i + 1)

            if data[1] != "0":
                self.links[link_id].left_link = data[1]
                self.links[data[1]].right_link = link_id
            if data[2] != "0":
                self.links[link_id].right_link = data[2]
                self.links[data[2]].left_link = link_id
            if data[3] != "0":
                self.links[link_id].through_link = data[3]
                self.links[data[3]].through_link = link_id

    def setup_lights(self):
        # Setup nodes
        for data in light_data:
            link_id = data[0]
            for light in data[1:]:
                self.links[link_id].lights.append(Light(*light.split(',')))

    def update_lights(self):
        for link in self.links.values():
            link.update_lights(self.time)

    def update_cars(self):
        self.rule.update_cars()

    def update_links(self):
        self.rule.update_links()

    # outputs
    def print_status(self):
        print "==== Time Stamp %d =====" % self.time
        for link in self.links.values():
            link.print_lights()

if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()