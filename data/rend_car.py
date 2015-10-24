__author__ = 'hongyusong'

import random

od_pairs = {}
time_interval = 100
car_num_eff = .17


def rend_car():
    fin = open('path.csv')
    fin.readline()
    fout = open('car.csv', 'w')
    fout.write('Car id,Start time,path' + "\n")

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
    rend_car()