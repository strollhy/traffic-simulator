import uuid
from model.link import Link
from model.sublink1 import SubLink1


class Factory(object):
    @classmethod
    def random_uuid(cls):
        return str(uuid.uuid1())

    @classmethod
    def create(cls, class_name):
        constructor = globals()[class_name + "Factory"]
        return constructor.create()


class LinkFactory(Factory):
    @classmethod
    def create(cls):
        link = Link()
        link.link_id = cls.random_uuid()
        link.sublink1 = SubLink1(link, 5)
        return link