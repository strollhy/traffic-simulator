from simulator import Simulator
from util.observer import Observer


ROUNDS = 1


class LoadBalancer(Observer):
    def __init__(self, rounds):
        self.simulate_rounds = rounds

        self.simulator = Simulator()
        self.simulator.mute = True

    def start(self):
        for _ in xrange(self.simulate_rounds):
            self.simulator.start()
            # TODO post simulation, recalculate path cost


if __name__ == "__main__":
    LoadBalancer(ROUNDS).start()