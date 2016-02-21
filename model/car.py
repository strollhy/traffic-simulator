from system.observer import Observable


class Car(Observable):
    def __init__(self):
        super(Car, self).__init__()

        self.car_id = None
        self.start_time = None
        self.path = None

        self.current_step = 0
        self.distance = 0
        self.arrive_time = 0
        self.lane_group = None

        self.is_blocked = False
        self.blocked_count = 0

    def __repr__(self):
        return "%s, %s" % (self.car_id, self.path)

    @property
    def next_link(self):
        return self.path[self.current_step] if not self.reach_destination() else None

    def reach_destination(self):
        if self.current_step >= len(self.path):
            self.notify_observers("Car #%s reaches its destination" % self.car_id)
            return True
        return False

    def move_on(self):
        self.current_step += 1

    def set_blocked(self, msg=""):
        self.is_blocked = True
        self.blocked_count += 1
        self.notify_observers("Car #%s is blocked to %s, %s. {%s}"
                              % (self.car_id, self.next_link, self.lane_group, msg))

    def unset_blocked(self):
        self.is_blocked = False
        self.block_count = 0