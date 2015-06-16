__author__ = 'hongyusong'

from traffic import *
from rule import Rule

######################################################
fake_data = dict()
fake_data["cars"] = [[1, "1,2", 0],
                     [2, "2,3", 1],
                     [3, "3,2", 10]]
fake_data["links"] = [[1, 1000, 4, 20, 50, 220, 4, 5, 5],
                      [2, 800, 4, 20, 50, 220, 4, 5, 5],
                      [3, 900, 4, 20, 50, 220, 4, 5, 5]]
fake_data["link_link"] = [[1, 2, 0, 0],
                          [2, 0, 0, 3],
                          [3, 0, 0, 0]]
fake_data["lights"] = [[1, "40,30", "50,50", "30,40"],
                       [2, "40,30", "50,50", "30,40"],
                       [3, "40,30", "50,50", "30,40"],]

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
        # TODO load from files
        self.next_time_stamp()

    def next_time_stamp(self):
        self.update_lights()
        self.update_cars()
        self.update_links()
        self.time += 1

    def setup_cars(self):
        # Setup cars
        for data in fake_data["cars"]:
            self.cars[data[0]] = Car(data)

    def setup_links(self):
        # Setup links
        for data in fake_data["links"]:
            self.links[data[0]] = Link(data)

        # Setup link connections
        for data in fake_data["link_link"]:
            link_id = data[0]
            if data[1]:
                self.links[link_id].left_link = data[1]
                self.links[data[1]].right_link = link_id
            if data[2]:
                self.links[link_id].right_link = data[2]
                self.links[data[2]].left_link = link_id
            if data[3]:
                self.links[link_id].through_link = data[3]
                self.links[data[3]].through_link = link_id

    def setup_lights(self):
        # Setup nodes
        for data in fake_data["lights"]:
            link_id = data[0]
            for light_data in data[1:]:
                self.links[link_id].lights.append(Light(*light_data.split(',')))

    def update_lights(self):
        for link in self.links.values():
            link.update_lights()

    def update_cars(self):
        self.rule.update_cars()

    def update_links(self):
        self.rule.update_links()


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()