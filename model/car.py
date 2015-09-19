__author__ = 'hongyusong'


class Car():
    def __init__(self, car_id, start_time, path):
        self.car_id = car_id
        self.path = path.split("-")
        self.start_time = int(start_time)
        self.distance = 0
        self.arrive_time = 0
        self.lane_group = None
        self.is_blocked = False

    def update_path(self):
        if self.path:
            self.path.pop(0)

    def update_arrive_time(self, arrive_time):
        self.arrive_time = arrive_time

    def get_destination(self):
        if not self.path:
            return None
        return self.path[0]