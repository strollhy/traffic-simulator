import random
from util.observer import Observable

od_pairs = {}
time_interval = 100
CAR_NUM_EFF = .017
INPUT_FILENAME = "../data/output/seed_path.csv"


class TrafficGenerator(Observable):
    def __init__(self, filename=INPUT_FILENAME):
        super(TrafficGenerator, self).__init__()
        self.filename = filename

    def generate_traffic(self, car_num_eff=CAR_NUM_EFF):
        self.notify_observers("========== Start generating traffic ==========")
        fin = open(self.filename)
        fout = open('../data/output/car.csv', 'w')
        fout.write('car_id,start_time,path' + "\n")

        car_id = 1
        fin.readline()
        for line in fin:
            path, car_num = line.strip().split(',')
            for _ in xrange(int(int(car_num) * car_num_eff)):
                start_time = random.randint(0, 180)
                fout.write("%d,%d,%s\n" % (car_id, start_time, path))
                car_id += 1
        self.notify_observers("========== Generating finished, %d cars created ==========" % car_id)
        fin.close()

    def rend_car_old(self, car_num_eff=CAR_NUM_EFF):
        fin = open('../data/old_path.csv')
        fin.readline()
        fout = open('../data/output/car.csv', 'w')
        fout.write('car_id,start_time,path' + "\n")

        for line in fin:
            data = line.strip().split(',')
            od, car_num, path, distance = data

            # TODO calculate distribution based on distance instead
            if od in od_pairs:
                od_pairs[od].append(data)
            else:
                od_pairs[od] = [data]

        car_id = 1
        car_num = 0
        for od, path_group in od_pairs.items():
            for data in path_group:
                od = data[0]
                car_num = data[1] if data[1] else car_num
                path = data[2]
                distance = data[3]
                for _ in xrange(int(int(car_num) * car_num_eff/len(path_group))):
                    start_time = random.randint(0, 100)
                    fout.write("%d,%d,%s\n" % (car_id, start_time, path))
                    car_id += 1

        fin.close()
        fout.close()

if __name__ == '__main__':
    TrafficGenerator().generate_traffic()