__author__ = 'hongyusong'

from model.link import *
from model.car import *
from model.observer import Observer

data_source = "data"


class Simulator(Observer):
    def __init__(self):
        self.time = 0
        self.total_time = 0
        self.cars = {}
        self.links = {}
        self.setup_links()
        self.setup_cars()
        self.setup_lights()

    def start(self):
        # initialize links
        self.update_links()

        # start simulation
        while self.total_time > self.time:
            self.next_time_stamp()

    def next_time_stamp(self):
        self.print_status()
        self.update_time()
        self.release_cars()
        self.update_links()

    def setup_cars(self):
        # Setup cars
        f = open(data_source + '/car.csv')
        f.readline()
        for line in f:
            data = line.strip().split(',')
            car = Car(*data)
            car.register_observer(self)
            self.cars[data[0]] = car

    def setup_links(self):
        # Setup links
        f = open(data_source + '/link.csv')
        f.readline()
        for line in f:
            link_data = line.strip().split(',')
            link_id = link_data[0]
            self.links[link_id] = MainLink(*link_data)
            self.links[link_id].register_observer(self)

        # Setup link connections
        f = open(data_source + '/link2link.csv')
        f.readline()
        for line in f:
            link2link = line.strip().split(',')
            link_id = link2link[0]
            if link_id not in self.links:
                continue

            if link2link[1] != '0' and link2link[1] in self.links:
                self.links[link_id].next_link["L"] = self.links[link2link[1]]
            if link2link[2] != '0' and link2link[2] in self.links:
                self.links[link_id].next_link["R"] = self.links[link2link[2]]
            if link2link[3] != '0' and link2link[3] in self.links:
                self.links[link_id].next_link["T"] = self.links[link2link[3]]
            if link2link[4] != '0' and link2link[4] in self.links:
                self.links[link_id].conflict_link = self.links[link2link[3]]

    def setup_lights(self):
        # Setup nodes
        f = open(data_source + '/signal_2.csv')
        f.readline()
        for line in f:
            data = line.strip().split(',')
            link_id = data[0] if data[0] else link_id
            direction = data[1]
            if direction in ["T", "R", "L"]:
                self.links[link_id].sublink3.setup_signal(direction, data[2:])
        self.total_time = len(data[2:])

    def update_time(self):
        for link in self.links.values():
            link.update_time(self.time)

        for car in self.cars.values():
            if self.time == car.start_time:
                link_id = car.path[0]
                self.links[link_id].add_car(car)

        self.time += 1

    def release_cars(self):
        for link in self.links.values():
            link.release_cars()

        # reset link status after release
        for link in self.links.values():
            link.post_release()

    def update_links(self):
        for link in self.links.values():
            link.update_status()

    # outputs
    def print_status(self):
        print "==== Time Stamp %ds =====" % (self.time * 10)


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()