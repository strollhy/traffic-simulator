from model.link import *
from util.observer import Observer
from reader.link_reader import LinkReader
from reader.link2link_reader import Link2LinkReader
from reader.car_reader import CarReader
from reader.signal_reader import SignalReader
from reader.path_reader import PathReader

from helper.traffic_generator import *


class Simulator(Observer):
    def __init__(self):
        super(Simulator, self).__init__()
        Time()
        self.total_time = 1000
        self.cars = []
        self.links = {}
        self.paths = {}

        self.path_reader = PathReader()
        self.traffic_generator = TrafficGenerator()

    def start(self):
        self.setup_system()
        self.init_links()
        self.start_simulation()

    def setup_system(self):
        self.traffic_generator.register_observer(self)
        self.traffic_generator.generate_traffic(time_interval=self.total_time-200, car_num_eff=.2)

        self.setup_links()
        self.setup_link2links()
        self.setup_cars()
        self.setup_signal()
        self.setup_paths()

    def setup_links(self):
        for link in LinkReader().links:
            link.simulator = self
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

    def setup_signal(self):
        for signal in SignalReader().signals:
            for lane in self.links[signal.link_id].sublink3.lanes:
                if set(signal.lane_type.upper()) & set(lane.type):
                    lane.signal = signal

    def setup_paths(self):
        for path in self.path_reader.paths:
            od = path.nodes[0], path.nodes[-1]
            if od in self.paths:
                self.paths[od][path.__str__()] = path
            else:
                self.paths[od] = {path.__str__(): path}

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

    def print_status(self):
        self.notify(None, "==== Time Stamp %ds =====" % (Time().time * Time().time_stamp))

    def unleash_cars(self):
        i = len(self.cars) - 1
        while i >= 0 and self.cars[i].start_time <= Time().time:
            if self.links[self.cars[i].current_link].capacity > 0:
                car = self.cars.pop(i)
                self.links[car.current_link].add_car(car)
            i -= 1

    def release_cars(self):
        released_links = set()
        for link in self.links.values():
            if link.type != "out" and link.link_id not in released_links:
                link.release_cars()
                released_links.add(link)
                released_links.add(link.conflict_link)

        # reset link status after release
        for link in self.links.values():
            link.post_release()

    def update_links(self):
        for link in self.links.values():
            link.update_status()


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()
