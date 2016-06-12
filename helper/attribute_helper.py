class AttributeHelper:
    @staticmethod
    def assign_attribute(obj, args):
        for key, val in args.items():
            try:
                val = float(val) if "." in val else int(val)
            except:
                pass
            finally:
                setattr(obj, key, val)
        return obj
