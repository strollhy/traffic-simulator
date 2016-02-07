from system.observer import Observable
from helper.attribute_helper import AttributeHelper


class Car(Observable):
    def __init__(self, args={}):
        super(Car, self).__init__()

        self.car_id = None
        self.start_time = None
        self.path = None
        AttributeHelper.assign_attribute(self, args)

        self.destination = self.path[-1]
        self.current_step = 0
        self.distance = 0
        self.arrive_time = 0
        self.lane_group = None

        self.is_blocked = False
        self.block_count = 0

    def __repr__(self):
        return "%s, %s" % (self.car_id, self.path)

    def move_on(self):
        self.current_step += 1
        if self.current_step >= len(self.path):
            # TODO reach destination
            pass

    def set_blocked(self, msg=""):
        self.is_blocked = True
        self.blocked_count += 1
        self.notify_observers("Car #%s is blocked to %s, %s. {%s}"
                              % (self.car_id, self.get_destination(), self.lane_group, msg))

    def unset_blocked(self):
        self.is_blocked = False
        self.block_count = 0