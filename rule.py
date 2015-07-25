__author__ = 'hongyusong'


class Rule():
    def __init__(self, simulator):
        self.simulator = simulator
        self.setup()

    def setup(self):
        # calculate all statuses
        self.update_links()

    def update_cars(self):
        for link in self.simulator.links.values():
            link.sublink3.release_cars()
            link.sublink2.update_cars()
            link.sublink1.update_cars()

    def update_links(self):
        for link in self.simulator.links.values():
            link.update_status()



