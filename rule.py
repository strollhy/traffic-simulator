__author__ = 'hongyusong'


class Rule():
    def __init__(self, simulator):
        self.simulator = simulator
        self.setup()

    def setup(self):
        # calculate all statuses
        self.update_cars()
        self.update_links()

    def update_cars(self):
        # update car status based on node&link status
        pass

    def update_links(self):
        # update link based on car status
        pass

    def cal_density(self, link):
        N = link.num_of_cars
        x = link.sublink_1 + link.sublink_2
        n = link.num_of_lanes
        l = link.length
        rho_jam = 220
        rho = (N-x)/(n*l-x/rho_jam)
        return rho

    def cal_velocity(self, link):
        v_min = link.min_speed
        v_free = link.max_speed
        rho = self.cal_density(link)
        rho_jam = 220
        alpha = 1.2
        beta = 1.8
        v = v_min + (v_min+v_free) * (1-(rho/rho_jam)**alpha)**beta
        return v



