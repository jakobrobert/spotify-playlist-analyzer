class AttributeDistributionInterval:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.count = 0
        self.percentage = 0

    def update_percentage(self, total_count):
        self.percentage = 100 * self.count / total_count

    # TODO there is a bug, values are now different than with version before
    def is_value_in_interval(self, value):
        if self.min_value is None and self.max_value is None:
            return True
        if self.min_value is None:
            return value <= self.max_value
        if self.max_value is None:
            return value <= self.min_value

        return self.min_value <= value <= self.max_value
