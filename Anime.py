class Anime:
    def __init__(self, title, genres, format, animeStatus, episodeCount, 
                 countryOfOrigin, userStatus, score, progress, repeats, startYear, 
                 startMonth, startDay, endYear, endMonth, endDay, notes):
        self.title = title
        self.genres = genres
        self.format = format
        self.animeStatus = animeStatus
        self.episodeCount = episodeCount
        self.countryOfOrigin = countryOfOrigin
        self.userStatus = userStatus
        self.score = score
        self.progress = progress
        self.repeats = repeats
        self.startDate = None
        if startYear == None and startMonth == None and startDay == None:
            self.startDate = "No date"
        else:
            self.startDate = str(startMonth) + "/" + str(startDay) + "/" + str(startYear)
        self.endDate = None
        if endYear == None and endMonth == None and endDay == None:
            self.endDate = "No Date"
        else:
            self.endDate = str(endMonth) + "/" + str(endDay) + "/" + str(endYear)
        self.notes = notes

    def __repr__(self):
        return str(self.title)

    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError
        if other.score == self.score:
            return self.title < other.title
        return other.score < self.score