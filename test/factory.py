import uuid
import random
from model.car import Car
from model.link import Link
from model.sublink1 import SubLink1
from model.sublink2 import SubLink2


def random_uuid():
    return str(uuid.uuid1())


class Factory(object):
    @classmethod
    def create(cls, class_name):
        constructor = globals()[class_name + "Factory"]
        return constructor.create()


class CarFactory(Factory):
    @classmethod
    def create(cls):
        car = Car()
        car.car_id = random_uuid()
        car.start_time = random.randint(0, 100)
        car.path = []
        return car


class LinkFactory(Factory):
    @classmethod
    def create(cls):
        link = Link()
        link.link_id = random_uuid()
        link.sublink1 = SubLink1(link, 5)
        link.sublink2 = SubLink2(link, 5)
        return link