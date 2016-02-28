from data_reader import DataReader
from model.car import Car
from helper.attribute_helper import AttributeHelper

CARS = '../data/output/car.csv'


class CarReader(DataReader):

    def __init__(self, filename=CARS):
        super(CarReader, self).__init__(filename)

        self._cars = None

    @property
    def cars(self):
        if self._cars is None:
            self._cars = []
            for row in self:
                self._cars.append(self.create_car(row))
        return self._cars

    @staticmethod
    def create_car(args):
        args['path'] = [int(p) for p in args['path'].split('-')]
        return AttributeHelper.assign_attribute(Car(), args)

if __name__ == "__main__":
    reader = CarReader()

    import pprint
    pprint.pprint(reader.cars)