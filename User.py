class User:
    def __init__(self, name, id, animeList, animeCount, animeMeanScore, 
                 animeStDev, animeMinWatched, animeEpisodesWatched, 
                 animeGenres, animeTags, mangaList, mangaCount,
                 mangaMeanScore, mangaStDev, mangaChaptersRead,
                 mangaVolumesRead, mangaGenres, mangaTags):
        self.name = name
        self.id = id
        self.animeList = animeList
        self.animeCount = animeCount
        self.animeMeanScore = animeMeanScore
        self.animeStDev = animeStDev
        self.animeMinWatched = animeMinWatched
        self.animeDaysWatched = round((self.animeMinWatched / 60) / 24, 2)
        self.animeEpisodesWatched = animeEpisodesWatched
        self.animeGenres = animeGenres
        self.animeTags = animeTags
        self.mangaList = mangaList
        self.mangaCount = mangaCount
        self.mangaMeanScore = mangaMeanScore
        self.mangaStDev = mangaStDev
        self.mangaChaptersRead = mangaChaptersRead
        self.mangaVolumesRead = mangaVolumesRead
        self.mangaGenres = mangaGenres
        self.mangaTags = mangaTags

    def __repr__(self):
        return str(self.name)