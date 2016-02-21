from data_reader import DataReader
from model.link import Link
from model.sublink1 import SubLink1
from model.sublink2 import SubLink2
from model.sublink3 import SubLink3
from helper.attribute_helper import AttributeHelper


LINKS = "../data/link.csv"


class LinkReader(DataReader):

    def __init__(self, path=LINKS):
        super(LinkReader, self).__init__(path)

        self._links = None

    @property
    def links(self):
        if self._links is None:
            self._links = []
            for row in self:
                link = self.create_link(row)
                if link:
                    self._links.append(link)
        return self._links

    @staticmethod
    def create_link(args):
        # change to miles, if no length is provided, assume infinite
        args["length"] = float(args["length"]) * 0.000189394 if args["length"] else 200
        args["max_cap"] = int(args["length"] / 0.00279617)

        link = Link()
        LinkReader.create_sublinks(link, args)
        return AttributeHelper.assign_attribute(link, args)

    @staticmethod
    def create_sublinks(link, args):
        lane_num = max(1, len([x for x in [args["L"], args["T1"], args["T2"], args["R"]] if int(x) > 0]) - 1)
        link.sublink1 = SubLink1(link, lane_num)
        link.sublink2 = SubLink2(link, lane_num)
        link.sublink3 = SubLink3(link, [args["L"], args["T1"], args["T2"], args["R"]])

if __name__ == "__main__":
    reader = LinkReader()

    import pprint
    pprint.pprint(reader.links)
