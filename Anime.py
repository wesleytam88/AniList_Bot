class Anime:
    def __init__(self, idAni, idMal, title, genres, format, animeStatus, 
                 episodeCount, countryOfOrigin, userStatus, score, progress, 
                 repeats, startYear, startMonth, startDay, endYear, endMonth, 
                 endDay, notes, customList):
        self.idAni: int = idAni
        self.idMal: int = idMal
        self.title: str = title
        self.genres: list[str] = genres
        self.format: str = format
        self.animeStatus: str = animeStatus
        self.episodeCount: int = episodeCount
        self.countryOfOrigin: str = countryOfOrigin
        self.userStatus: str = userStatus
        self.score = score
        self.progress: int = progress
        self.repeats: int = repeats

        # Start-date formatting
        self.startDate = None
        if startYear == None and startMonth == None and startDay == None:
            self.startDate = "No date"
        else:
            self.startDate = f"{startMonth}/{startDay}/{startYear}"

        # End-date formatting
        self.endDate = None
        if endYear == None and endMonth == None and endDay == None:
            self.endDate = "No Date"
        else:
            self.endDate = f"{endMonth}/{endDay}/{endYear}"

        self.notes: str = notes
        self.customList: list[str] = customList

    def __repr__(self):
        return str(self.title)

    def __lt__(self, other):
        # Default sort by score, then alphabetical
        if type(other) != type(self):
            raise TypeError
        if other.score == self.score:
            return self.title.lower < other.title.lower
        return other.score < self.score