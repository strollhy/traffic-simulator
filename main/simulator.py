from model.link import *
from model.car import *

from system.observer import Observer
from reader.link_reader import LinkReader
from reader.link2link_reader import Link2LinkReader
from reader.car_reader import CarReader


class Simulator(Observer):
    def __init__(self):
        self.time = 0
        self.total_time = 0
        self.cars = {}
        self.links = {}

    def start(self):
        # Setup data
        self._setup_system()

        # initialize links
        self.update_links()

        # start simulation
        while self.total_time > self.time:
            self.next_time_stamp()

    def _setup_system(self):
        self.setup_links()
        self.setup_link2links()
        self.setup_cars()
        self.setup_lights()

    def setup_links(self):
        for link in LinkReader().links:
            self.links[link.link_id] = link
            self.links[link.link_id].register_observer(self)

    def setup_link2links(self):
        for link2link in Link2LinkReader().link2links:
            link_id = link2link.link_id

            if link2link.left_link_id and link2link.left_link_id in self.links:
                self.links[link_id].next_link["L"] = self.links[link2link.left_link_id]
            if link2link.right_link_id and link2link.right_link_id in self.links:
                self.links[link_id].next_link["R"] = self.links[link2link.right_link_id]
            if link2link.through_link_id and link2link.through_link_id in self.links:
                self.links[link_id].next_link["T"] = self.links[link2link.through_link_id]
            if link2link.conflict_link_id and link2link.conflict_link_id in self.links:
                self.links[link_id].conflict_link = self.links[link2link.conflict_link_id]

    def setup_cars(self):
        for car in CarReader().cars:
            car.register_observer(self)
            self.cars[car.car_id] = car

    def setup_lights(self):
        # TODO replace with
        f = open('../data/signal_2.csv')
        f.readline()
        for line in f:
            data = line.strip().split(',')
            link_id = data[0] if data[0] else link_id
            link_id = int(link_id)
            direction = data[1]
            if direction in ["T", "R", "L"]:
                self.links[link_id].sublink3.setup_signal(direction, data[2:])
        self.total_time = len(data[2:])

    def next_time_stamp(self):
        self.print_status()
        self.update_time()
        self.release_cars()
        self.update_links()

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