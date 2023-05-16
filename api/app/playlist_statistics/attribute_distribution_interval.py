class AttributeDistributionInterval:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.count = 0
        self.percentage = 0

    def update_percentage(self, total):
        self.percentage = 100 * self.count / total

    # TODO Add method to check if value is in interval
    # TODO maybe add more high level method update_count(all_values)
        # -> e.g. it contains release_year values of all tracks, then counts how many are within this interval
