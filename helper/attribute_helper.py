class AttributeHelper:
    @staticmethod
    def assign_attribute(obj, args):
        for key, val in args.items():
            setattr(obj, key, val)