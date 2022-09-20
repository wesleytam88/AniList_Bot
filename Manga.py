from email.errors import StartBoundaryNotFoundDefect


class Manga:
    def __init__(self, title, genres, format, mangaStatus, chapterCount, 
                 volumeCount, countryOfOrigin, userStatus, score, progress, progressVolumes, repeats, 
                 startYear, startMonth, startDay, endYear, endMonth, endDay, notes):
        self.title = title
        self.genres = genres
        self.format = format
        self.mangaStatus = mangaStatus
        self.chapterCount = chapterCount
        self.volumeCount = volumeCount
        self.countryOfOrigin = countryOfOrigin
        self.userStatus = userStatus
        self.score = score
        self.progress = progress
        self.progressVolumes = progressVolumes
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
        if self.score == other.score:
            return self.title < other.title
        return other.score < self.score