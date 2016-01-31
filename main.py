__author__ = 'hongyusong'

from model.link import *
from model.car import *
from model.observer import Observer
from model.path import Path
from rend_car import rend_car
import math

data_source = "data"


class Simulator(Observer):
    def __init__(self, step):
        self.time = 0
        self.total_time = 0
        self.cars = {}
        self.links = {}
        self.ods = {}
        self.step = step
        self.paths = {}
        self.setup_links()
        self.setup_paths()
        self.setup_cars()
        self.setup_lights()

    def start(self):
        # initialize links
        self.update_links()

        # start simulation
        while self.total_time > self.time:
            self.next_time_stamp()

        self.post_simulate()

    def post_simulate(self):
        print self.step
        fout = open('data/path.csv', 'w')

        a = 0
        b = 0
        all_total = 0
        new_total = 0
        for od, paths in self.paths.items():
            # for each path with the same od pair
            total_num = 0
            new_total_num = 0
            step = self.step + 9
            min_cost = 999999999

            sorted_path = sorted([path for path in paths.values()], key=lambda x: x.avg_time())
            total_num = sum([path.car_num for path in sorted_path])

            cached_num = []
            for i, path in enumerate(sorted_path):
                cost = path.avg_time()
                car_num = path.car_num

                if i == 0:
                    min_cost = cost
                    new_car_num = int(math.ceil((car_num * (step - 1.0) + total_num * 1.0) / step))
                elif 0 < i < len(sorted_path) / 2:
                    new_car_num = int(math.ceil(car_num * (step - 1.0) / step))
                else:
                    new_car_num = int(math.floor(car_num * (step - 1.0) / step))

                new_total_num += new_car_num
                # fout.write('-'.join(path.nodes) + ',' + str(new_car_num) + "\n")
                cached_num.append(new_car_num)
                a += cost * new_car_num

            b += min_cost * new_total_num
            all_total += total_num
            new_total += new_total_num

            # print total_num, new_total_num
            lost = total_num - new_total_num
            while lost != 0:
                for i in xrange(len(cached_num)):
                    cached_num[i] += lost/abs(lost)
                    lost += - lost/abs(lost)
                    if lost == 0:
                        break

            for i, path in enumerate(sorted_path):
                fout.write('-'.join(path.nodes) + ',' + str(cached_num[i]) + "\n")

            # for path in paths.values():
            #     if not path.elapse_time:
            #         continue
            #     cost = path.avg_time()
            #     # cost = 0
            #     # nodes, car_num = path
            #     # for node in path.nodes:
            #     #     if self.links[node].passed_cars:
            #     #         cost += self.links[node].passed_time / self.links[node].passed_cars
            #     #     if
            #
            #     min_cost = min(cost, min_cost)
            #     total_num += path.car_num
            #
            # # calculate each portion
            # new_total_num = 0
            # for path in paths.values():
            #     if not path.elapse_time:
            #         continue
            #
            #     cost = path.avg_time()
            #     # cost = 0
            #     # nodes, car_num = path
            #     # for node in nodes:
            #     #     if self.links[node].passed_cars:
            #     #         cost += self.links[node].passed_time / self.links[node].passed_cars
            #
            #     car_num = path.car_num
            #     new_car_num = int(round(car_num * (step - 1.0) / step))
            #     print car_num, new_car_num, cost, min_cost
            #     if cost == min_cost:
            #          new_car_num += total_num / step
            #
            #     new_total_num += new_car_num
            #     if new_car_num > 0:
            #         fout.write('-'.join(path.nodes) + ',' + str(new_car_num) + "\n")
            #         a += cost * new_car_num

        print a, b
        print (a - b) / (b + 0.1)
        print all_total, new_total
        fout.close()
        # render car again from the path
        rend_car('data/path.csv')

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

            od = car.path[0] + '-' + car.path[-1]
            if od in self.ods:
                self.ods[od].add(data[-1])
            else:
                self.ods[od] = set(data[-1])

        if not self.cars:
            exit()

    def setup_links(self):
        # Setup links
        f = open(data_source + '/link.csv')
        f.readline()
        for line in f:
            link_data = line.strip().split(',')
            link_id = link_data[0]
            self.links[link_id] = MainLink(self, *link_data)
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

    def setup_paths(self):
        if self.step == 1:
            f = open(data_source + '/allocation_path.csv')
            rend_car(data_source + '/allocation_path.csv')
        else:
            f = open(data_source + '/path.csv')

        for line in f:
            path, car_num = line.strip().split(',')
            car_num = int(car_num)
            nodes = path.split('-')
            od = nodes[0], nodes[-1]
            if od in self.paths:
                self.paths[od][path] = Path(nodes, car_num)
            else:
                self.paths[od] = {path: Path(nodes, car_num)}


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
        # print "==== Time Stamp %ds =====" % (self.time * 10)
        pass


if __name__ == '__main__':
    N = 50
    for step in xrange(1, N):
        simulator = Simulator(step)
        simulator.start()