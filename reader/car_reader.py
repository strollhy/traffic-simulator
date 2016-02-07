from data_reader import DataReader

CARS = '../data/car.csv'


class CarReader(DataReader):

    def __init__(self, path):
        super(CarReader, self).__init__(path)

        self._cars = None

    @property
    def cars(self):
        if self._cars is None:
            self._cars = []
            for row in self:
                self._cars.append(row)
        return self._cars


if __name__ == "__main__":
    reader = CarReader(CARS)

    import pprint
    pprint.pprint(reader.cars)
