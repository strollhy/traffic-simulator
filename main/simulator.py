from model.link import *
from util.observer import Observer
from reader.link_reader import LinkReader
from reader.link2link_reader import Link2LinkReader
from reader.car_reader import CarReader
from helper.traffic_generator import *


class Simulator(Observer):
    def __init__(self):
        Time()
        self.total_time = 0
        self.cars = []
        self.links = {}

    def start(self):
        self.setup_system()
        self.init_links()
        self.start_simulation()

    def setup_system(self):
        self.traffic_generator = TrafficGenerator()
        self.traffic_generator.register_observer(self)
        self.traffic_generator.generate_traffic(car_num_eff=.1)

        self.setup_links()
        self.setup_link2links()
        self.setup_cars()
        self.setup_signals()

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
            self.cars.append(car)

        self.cars.sort(key=lambda c: c.start_time, reverse=True)

    def setup_signals(self):
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

    def init_links(self):
        self.update_links()

    def start_simulation(self):
        while self.total_time > Time().time:
            self.next_time_stamp()

    def next_time_stamp(self):
        self.print_status()
        self.unleash_cars()
        self.release_cars()
        self.update_links()
        Time().update_time()

    @staticmethod
    def print_status():
        print "==== Time Stamp %ds =====" % (Time().time * 10)

    def unleash_cars(self):
        while self.cars and self.cars[-1].start_time <= Time().time:
            car = self.cars.pop()
            self.links[car.path[0]].add_car(car)

    def release_cars(self):
        for link in self.links.values():
            link.release_cars()

        # reset link status after release
        for link in self.links.values():
            link.post_release()

    def update_links(self):
        for link in self.links.values():
            link.update_status()


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()