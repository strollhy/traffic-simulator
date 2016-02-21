from sublink import SubLink

class SubLink2(SubLink):
    def __init__(self, link, lane_num):
        SubLink.__init__(self, link, lane_num)
        self.allowed_merge = {"L": lane_num, "R": lane_num, "T": lane_num}
        self.pass_count = 0

    def add_car(self, car, from_lane):
        # if car reaches the zone
        if self.in_zone(car):
            self.lanes[from_lane].append(car)
            car.distance = 0
            self.pass_count += 1
            return True
        return False

    def in_zone(self, car):
        car.distance += self.link.avg_speed * 10.0 / 3600
        return car.distance > self.get_abscissa() or self.link.length >= 200

    def get_abscissa(self):
        return self.link.length - max([len(l) for l in self.lanes]) / self.link.jam_density

    def release_cars(self, car_per_line):
        self.update_allowed_merge()

        for _ in xrange(car_per_line):
            for lane_number, lane in enumerate(self.lanes):
                # skip if either lane is empty or first car is block
                if not lane or lane[0].is_blocked:
                    continue

                car = lane[0]
                # if allow merged on this lane group and also find an empty space
                if self.allowed_merge[car.lane_group] > 0:
                    available_lane = self.link.sublink3.find_available_lanes(car.lane_group, lane_number)
                    if available_lane:
                        # if there is a lane directly accessible, then release the car
                        self.__release_car(lane_number, available_lane[0])
                    else:
                        car.set_blocked("No space left on merging zone. %d"
                                        % (self.link.sublink3.group_capacity(car.lane_group)))
                else:
                    car.set_blocked("Merging not allowed.")

        # reset car status for next time stamp
        for lane in self.lanes:
            for car in lane:
                car.unset_blocked()

    def __release_car(self, lane_number, next_lane):
        car = self.lanes[lane_number].pop(0)
        self.allowed_merge[car.lane_group] -= 1
        self.link.sublink3.add_car(car, next_lane)
        self.link.notify_observers("Adding car #%d to merging group %s, %d -> %d"
                                   % (car.car_id, car.lane_group, self.link.link_id, car.next_link))

    def update_allowed_merge(self):
        if not self.lanes:
            return

        for lane_group in self.allowed_merge.keys():
            if self.link.sublink3.single_lane:
                self.allowed_merge['T'] = 5
                self.allowed_merge['L'] = 3
                self.allowed_merge['R'] = 3
            else:
                blockage_factor = self.cal_blockage_factor(lane_group)
                self.allowed_merge[lane_group] = max(1 - blockage_factor, 0) * self.get_car_num()

    @staticmethod
    def count_cars_in_lane_group(lane, lane_group):
        return len([c for c in lane if lane_group == c.lane_group])

    def cal_blockage_factor(self, direction):
        if direction == "L":
            # if totally blocked on the group
            cnt_l = self.count_cars_in_lane_group(self.lanes[0], 'L')
            cnt_t = self.count_cars_in_lane_group(self.lanes[0], 'T')
            return cnt_t / (cnt_l + cnt_t + .1)

        elif direction == "R":
            cnt_l = self.count_cars_in_lane_group(self.lanes[0], "L")
            cnt_t = self.count_cars_in_lane_group(self.lanes[0], "T")

            cnt_t_2 = self.count_cars_in_lane_group(self.lanes[-1], "T")
            cnt_r = self.count_cars_in_lane_group(self.lanes[-1], "R")
            return cnt_l / (cnt_t + cnt_l + .1) + cnt_r / (cnt_t_2 + cnt_r + .1)

        elif "T" in direction:
            cnt_r = self.count_cars_in_lane_group(self.lanes[-1], 'R')
            cnt_t = self.count_cars_in_lane_group(self.lanes[-1], 'T')
            return cnt_t * 1.0 / (cnt_r + cnt_t + .1)