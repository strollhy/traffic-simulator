from reader.link_reader import LinkReader
from reader.link2link_reader import Link2LinkReader


class MapRender:
    def __init__(self):
        self.links = self.load_links()
        self.link2link_cost = self.load_link2link_cost()

    @staticmethod
    def load_links():
        links = {}
        for link in LinkReader().links:
            links[link.link_id] = link
        return links

    def load_link2link_cost(self):
        link2link_cost = []
        for link2link in Link2LinkReader().link2links:
            if link2link.left_link_id:
                link2link_cost.append(self.link2link_cost_row(link2link.link_id, link2link.left_link_id))
            if link2link.right_link_id:
                link2link_cost.append(self.link2link_cost_row(link2link.link_id, link2link.right_link_id))
            if link2link.through_link_id:
                link2link_cost.append(self.link2link_cost_row(link2link.link_id, link2link.through_link_id))
        return link2link_cost

    def link2link_cost_row(self, l1_id, l2_id):
        return [self.links[l1_id].normalized_id,
                self.links[l2_id].normalized_id,
                int(self.links[l1_id].length / 0.000189394)]

    def rend_graph_cost(self):
        out_file = open("../data/output/graph_cost", "w")
        out_file.write("%d\n\n" % len(self.link2link_cost))

        for l2l in self.link2link_cost:
            l1, l2, cost = l2l
            out_file.write("%d %d %d\n" % (l1, l2, cost))

    def rend_normalized_od(self):
        in_file = open("../data/output/ods.csv", "r")
        out_file = open("../data/normalized_od.csv", "w")
        for line in in_file:
            l1, l2, car_num = line.split(',')
            out_file.write("%s,%s,%s" % (self.links[int(l1)].normalized_id,
                                         self.links[int(l2)].normalized_id,
                                         car_num))

if __name__ == "__main__":
    map_render = MapRender()
    map_render.rend_graph_cost()
    map_render.rend_normalized_od()