class Link2Link(object):
    def __init__(self):
        self.link_id = None
        self.left_link_id = None
        self.right_link_id = None
        self.through_link_id = None
        self.conflict_link_id = None

    def __repr__(self):
        return "[%s: %s, %s, %s]" % (self.link_id, self.left_link_id, self.right_link_id, self.through_link_id)