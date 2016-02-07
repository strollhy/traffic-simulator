from data_reader import DataReader
from model.car import Car

CARS = '../data/car.csv'


class CarReader(DataReader):

    def __init__(self, path=CARS):
        super(CarReader, self).__init__(path)

        self._cars = None

    @property
    def cars(self):
        if self._cars is None:
            self._cars = []
            for row in self:
                row['path'] = row['path'].split('-')
                self._cars.append(Car(row))
        return self._cars


if __name__ == "__main__":
    reader = CarReader()

    import pprint
    pprint.pprint(reader.cars)