__author__ = 'hongyusong'

from traffic import *


class TrafficRule():
    def __init__(self):
        pass

######################################################


class Simulator():
    def __init__(self, init_data):
        self.time = 0

        # TODO init from data
        self.cars = []
        self.links = []
        self.nodes = []

    def start(self, data):
        for d in data:
            self.next_time_stamp(d)

    def next_time_stamp(self, d):
        self.update_nodes()
        self.update_links()
        self.update_cars()
        self.time += 1

    def update_nodes(self):
        pass

    def update_links(self):
        pass

    def update_cars(self):
        pass

######################################################


def load_init_data():
    return ''


def load_timestamp_data():
    return ''


if __name__ == '__main__':
    # TODO load input
    init_data = load_init_data()
    time_stamp = load_timestamp_data()

    # TODO start simulation here
    simulator = Simulator(init_data)
    simulator.start(time_stamp)