class Tag:
    def __init__(self, tag, count, meanScore):
        self.tag = tag
        self.count = count
        self.meanScore = meanScore

    def __repr__(self):
        return str(self.tag)

    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError
        return self.meanScore < other.meanScore