__author__ = 'hongyusong'

from traffic import *
from rule import Rule

######################################################
fake_data = dict()
fake_data["cars"] = [[1, "1-2", 1000],
                     [2, "2-3", 1001]]
fake_data["links"] = [[1, 1, 2, 1000, 4, 20, 50, 220, 4, 5, 5],
                      [2, 2, 3, 800, 4, 20, 50, 220, 4, 5, 5],
                      [3, 3, 4, 900, 4, 20, 50, 220, 4, 5, 5]]
fake_data["link_link"] = [[1, 2, 0, 0],
                          [2, 0, 0, 1],
                          [3, 0, 0, 0]]
fake_data["nodes"] = [[1, 1, 1, 1, 0, 1000],
                      [2, 2, 1, 1, 0, 1000],
                      [3, 3, 1, 1, 0, 1000],]

fake_data["timestamp"] = [[1, 0, 1, 1, 0, 1010],
                          [2, 1, 1, 1, 0, 1020],
                          [3, 2, 1, 1, 0, 1030]]
######################################################


class Simulator:
    def __init__(self):
        self.time = 0
        self.cars = {}
        self.links = {}
        self.nodes = {}
        self.setup_cars()
        self.setup_links()
        self.setup_nodes()
        self.rule = Rule(self)

    def start(self):
        # TODO load from files
        self.time_stamp = fake_data['timestamp']
        self.next_time_stamp()

    def next_time_stamp(self):
        self.update_nodes()
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

    def setup_nodes(self):
        # Setup nodes
        for data in fake_data["nodes"]:
            node_id = data[0]
            node = Node(data)
            self.nodes[node_id] = node
            self.links[data[1]].nodes[node_id] = node

    def update_nodes(self):
        for data in self.time_stamp:
            self.nodes[data[0]].update(data[2:5])

    def update_cars(self):
        self.rule.update_cars()

    def update_links(self):
        self.rule.update_links()


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()