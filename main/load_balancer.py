import math
from simulator import Simulator
from util.observer import Observer
from model.time import Time
from helper.traffic_generator import TrafficGenerator
from reader.path_reader import PathReader

TURNS = 20
TMP_PATH_FILE = '../data/output/balanced_path.csv'


class LoadBalancer(Observer):
    def __init__(self, turns):
        self.simulate_turns = turns

        self.simulator = Simulator()
        self.simulator.mute = True      # Disable system display

    def start(self):
        for turn in xrange(self.simulate_turns):
            print "========= Round %d =========" % turn

            self.simulator.start()
            self.post_simulation(turn)

            self.simulator.traffic_generator = TrafficGenerator(filename=TMP_PATH_FILE)
            self.simulator.path_reader = PathReader(TMP_PATH_FILE)
            Time().reset()

    def post_simulation(self, run):
        fout = open(TMP_PATH_FILE, 'w')
        fout.write("nodes,car_num\n")

        a = 0
        b = 0
        all_total = 0
        new_total = 0
        for od, paths in self.simulator.paths.items():
            # for each path with the same od pair
            new_total_num = 0
            od_total_num = 0
            step = run + 4

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
                # od_total_num += car_num
                cached_num.append(new_car_num)
                a += cost * new_car_num

            b += min_cost * new_total_num
            all_total += total_num
            new_total += new_total_num

            # lost = total_num - new_total_num
            # while lost != 0:
            #     for i in xrange(len(cached_num)):
            #         cached_num[i] += lost/abs(lost)
            #         lost += - lost/abs(lost)
            #         if lost == 0:
            #             break

            for i, path in enumerate(sorted_path):
                if cached_num[i]:
                    fout.write("%s,%d\n" % (path.__str__(), cached_num[i]))

        print a, b
        print (a - b) / (b + 0.1)
        print all_total, new_total
        fout.close()

if __name__ == "__main__":
    LoadBalancer(TURNS).start()