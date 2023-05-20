class AttributeDistributionInterval:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.count = 0
        self.percentage = 0

    def update_count(self, all_values):
        self.count = sum(self.__is_value_in_interval(value) for value in all_values)

    def update_percentage(self, total_count):
        if total_count == 0:
            self.percentage = 0
            return

        self.percentage = 100 * self.count / total_count

    def __is_value_in_interval(self, value):
        if self.min_value is None and self.max_value is None:
            return True
        if self.min_value is None:
            return value <= self.max_value
        if self.max_value is None:
            return value >= self.min_value

        return self.min_value <= value <= self.max_value
