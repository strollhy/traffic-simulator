from random import sample
from reader.link_reader import LinkReader

OUT_FILE_PATH = "../data/output/ods.csv"
OD_GROUP = "../data/od_hour2.csv"
LINK_GROUP = "../data/link_group.csv"

OD_NUM = 300
CAR_NUM = 18000


class OdGenerator:
    def __init__(self, outfile):
        self.outfile = open(outfile, "w")
        self.links = {"normal": [], "in": [], "out": []}

    # def run(self, od_num, car_num, ratio=.5):
    #     for link in LinkReader().links:
    #         self.links[link.type].append(link.link_id)
    #
    #     od_pairs = [sample(self.links["in"], 1) + sample(self.links["out"], 1) for _ in xrange(int(od_num * ratio))]
    #     od_pairs += [sample(self.links["normal"], 2) for _ in xrange(int(od_num * ratio))]
    #
    #     for od_pair in od_pairs:
    #         self.outfile.write("%s,%s,%d\n" % (od_pair[0], od_pair[1], int(car_num/od_num)))

    def rend_from_file(self):
        import csv
        zones = {}
        od_num = 10
        ratio = 0.7

        for row in csv.DictReader(open(LINK_GROUP)):
            link_id, zone_id, type = row["link_id"], row["zone"], row["type"]

            if row["zone"] not in zones:
                zones[row["zone"]] = {"in":[], "out":[], "normal":[]}
            zones[row["zone"]][row["type"]].append(row["link_id"])

        od_pairs = []
        for row in csv.DictReader(open(OD_GROUP)):
            zone_in, zone_out, car_num = row["in"], row["out"], int(row["num"])

            if zones[zone_in]["in"] and zones[zone_out]["out"]:
                od_pairs += [sample(zones[zone_in]["in"], 1) + sample(zones[zone_out]["out"], 1) + [car_num/od_num] for _ in xrange(od_num/4)]
                od_pairs += [sample(zones[zone_in]["normal"], 1) + sample(zones[zone_out]["out"], 1) + [car_num/od_num] for _ in xrange(od_num/4)]
                od_pairs += [sample(zones[zone_in]["in"], 1) + sample(zones[zone_out]["normal"], 1) + [car_num/od_num] for _ in xrange(od_num/4)]
                od_pairs += [sample(zones[zone_in]["normal"], 1) + sample(zones[zone_out]["normal"], 1) + [car_num/od_num] for _ in xrange(od_num/4)]
            else:
                od_pairs += [sample(zones[zone_in]["normal"], 1) + sample(zones[zone_out]["normal"], 1) + [car_num/od_num] for _ in xrange(od_num)]

        for od_pair in od_pairs:
            self.outfile.write("%s,%s,%d\n" % (od_pair[0], od_pair[1], od_pair[2]))


if __name__ == "__main__":
    # OdGenerator(OUT_FILE_PATH).run(OD_NUM, CAR_NUM)
    OdGenerator(OUT_FILE_PATH).rend_from_file()
