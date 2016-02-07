__author__ = 'hongyusong'

from system.observer import Observable
f = open('data/density.txt', 'w')


class MainLink(Observable):
    def __init__(self, *data):
        super(MainLink, self).__init__()
        self.link_id = data[0]
        self.length = float(data[1]) * 0.000189394 if data[1] else 200  # if no length is provided, assume infinite
        self.max_cap = int(self.length / 0.00279617)
        self.num_of_lanes = int(data[2])
        self.min_speed = int(data[3])
        self.max_speed = int(data[4])
        self.jam_density = int(data[5])
        self.time = 0

        self.next_link = {"T": None, "L": None, "R": None}
        self.conflict_link = None

        self.num_of_cars = 0
        self.capacity = 0
        self.avg_speed = 0
        self.lane_num = len(data[6:]) - 1
        self.sublink1 = SubLink1(self, self.lane_num)
        self.sublink2 = SubLink2(self, self.lane_num)
        self.sublink3 = SubLink3(self, data[6:])

    def update_time(self, time):
        self.time = time

    def add_car(self, car):
        """
        Add car to the main link

        :param car:
        :return:
        """
        self.notify_observers("Car #%s reaches link #%s" % (car.car_id, self.link_id))
        # update car status
        car.move_on()
        car.update_arrive_time(self.time)

        # check car status
        if not car.get_destination():
            self.notify_observers("Car #%s reaches its destination" % car.car_id)
            return

        # assign lane group to car
        if not self.assign_lane_group(car):
            self.notify_observers("Car #%s reaches dead end, couldn't find a path from %s to %s" % (car.car_id, self.link_id, car.get_destination()))
            return

        # add to sublink1
        self.sublink1.add_car(car)

    def assign_lane_group(self, car):
        heading_link = car.get_destination()
        for group, link in self.next_link.items():
            if link and link.link_id == heading_link:
                car.lane_group = group
                return True
        return False

    def update_status(self):
        self.cal_velocity()

    def get_capacity(self):
        return self.max_cap - self.sublink2.get_car_num() - self.sublink3.get_car_num() - self.sublink1.get_car_num()

    def cal_density(self):
        x = self.sublink2.get_car_num() + self.sublink3.get_car_num()
        N = x + self.sublink1.get_car_num()
        n = self.num_of_lanes
        l = self.length
        rho_jam = 220.0
        rho = (N-x)/(n*l-x/rho_jam + .1)
        f = open('data/density.txt', 'a')
        f.write("%s,%d,%d,%d,%f,%f,%d,%d\n" % (self.link_id, N, x, n, l, rho, self.sublink2.pass_count, self.time))
        f.close()
        return rho

    def cal_velocity(self):
        if self.length == 0: return
        v_min = self.min_speed
        v_free = self.max_speed
        rho = self.cal_density()
        rho_jam = 220.0
        alpha = 1.2
        beta = 1.8
        self.avg_speed = v_min + (v_free - v_min) * (1-(rho/rho_jam)**alpha)**beta

    def release_cars(self):
        self.sublink1.release_cars()
        self.sublink2.release_cars(10)
        self.sublink3.release_cars()

    def post_release(self):
        self.sublink3.post_release()