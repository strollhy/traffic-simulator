import random
from sublink import SubLink


class SubLink1(SubLink):
    def add_car(self, car):
        direction = car.lane_group
        if direction == "T":
            i = random.randint(0, len(self.lanes) - 1)
            self.lanes[i].append(car)
        elif direction == "R":
            self.lanes[-1].append(car)
        else:
            self.lanes[0].append(car)

    def release_cars(self):
        for lane_number, lane in enumerate(self.lanes):
            for car in lane:
                if self.link.sublink2.add_car(car, lane_number):
                    lane.remove(car)