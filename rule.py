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
