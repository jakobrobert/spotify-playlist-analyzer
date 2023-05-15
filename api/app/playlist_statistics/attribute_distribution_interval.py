class AttributeDistributionInterval:
    # TODO for now, is just a data container. Move logic into this class. e.g. update_percentage(total_count)
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.count = 0
