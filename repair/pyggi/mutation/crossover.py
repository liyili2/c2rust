class Crossover:
    def __init__(self, offspring_1, offspring_2, target_node):
        self.offspring_1 = offspring_1
        self.offspring_2 = offspring_2
        self.target_node = target_node
        return self.apply()

    def apply(self):
        # self.offspring_1.target = self.offspring_2.target
        return self.offspring_1, self.offspring_2
