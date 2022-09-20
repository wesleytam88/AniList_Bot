class Genre:
    def __init__(self, genre, count, meanScore):
        self.genre = genre
        self.count = count
        self.meanScore = meanScore

    def __repr__(self):
        return str(self.genre)

    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError
        return self.meanScore < other.meanScore