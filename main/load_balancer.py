from simulator import Simulator


ROUNDS = 1


class LoadBalancer(object):
    def __init__(self, rounds):
        self.simulator = Simulator()
        self.simulate_rounds = rounds

    def start(self):
        for _ in xrange(self.simulate_rounds):
            self.simulator.start()
            # TODO post simulation, recalculate path cost


if __name__ == "__main__":
    LoadBalancer(ROUNDS).start()