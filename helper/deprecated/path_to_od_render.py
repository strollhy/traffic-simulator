# transfor path file to od pair file for k-shortest path


def path_to_od():
    fin = open('../data/init_path.csv')
    fin.readline()
    fout = open('../data/output/od.csv', 'w')
    od_pairs = {}

    for line in fin:
        data = line.strip().split(',')
        od, car_num, path, distance = data

        if not car_num:
            continue

        path = path.split('-')
        fout.write("%s,%s,%s\n" % (path[0], path[-1], car_num))

    fin.close()
    fout.close()

if __name__ == '__main__':
    path_to_od()