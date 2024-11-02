import requests
from User import *
from Anime import *
from Manga import *
from Genre import *
from Tag import *
from OrderedList import *

# https://anilist.github.io/ApiV2-GraphQL-Docs/
# https://anilist.co/graphiql
URL = 'https://graphql.anilist.co'
STDLISTS = {"Watching", "Rewatching", "Completed", "Paused", "Dropped", "Planning"}

def create_vars(username):
    # Define our query variables and values that will be used in query request
    variables = {
        'name': username
    }
    return variables

query = '''
query ($name: String) {            # Define variables to be used in query (id)
    User (name: $name) {
        name
		id
		statistics {
			anime {
				count
                meanScore
                standardDeviation
                minutesWatched
                episodesWatched
                genres {
                    genre
                    count
                    meanScore
                }
                tags {
                    tag {
                        name
                    }
                    count
                    meanScore
                }
			}
            manga {
                count
                meanScore
                standardDeviation
                chaptersRead
                volumesRead
                genres {
                    genre
                    count
                    meanScore
                }
                tags {
                    tag {
                        name
                    }
                    count
                    meanScore
                }
            }
		}
	}
    anime: MediaListCollection(userName: $name, type: ANIME) {
        lists {
            name
            entries {
                media {
                    id
                    idMal
                    title {
                        english
                        romaji
                    }
                    genres
                    format
                    status
                    episodes
                    countryOfOrigin
                }
                status
                score
                progress
                repeat
                startedAt {
                    year
                    month
                    day
                }
                completedAt {
                    year
                    month
                    day
                }
                notes
            }
        }
    }
    manga: MediaListCollection(userName: $name, type: MANGA) {
        lists {
            name
            entries {
                media {
                    id
                    idMal
                    title {
                        english
                        romaji
                    }
                    genres
                    format
                    status
                    chapters
                    volumes
                    countryOfOrigin
                }
                status
                score
                progress
                progressVolumes
                repeat
                startedAt {
                    year
                    month
                    day
                }
                completedAt {
                    year
                    month
                    day
                }
                notes
            }
        }
    }
}
''' 

def animeList(username: str) -> dict[int, Anime]:
    '''Returns a hash table of a user's anime list. The anime's
    title, genres, format, animeStatus, episodeCount, countryOfOrigin,
    userStatus, and score are stored as the value, with the anime's
    title stored as the key
    '''
    animelist: dict[int: Anime] = {}
    variables: dict[str: str] = create_vars(username)
    response = requests.post(URL, json={'query':query, 'variables':variables})
    response = response.json()    # Turn json into hash table

    data = response['data']
    anime = data['anime']
    lists = anime['lists']
    for listType in lists:        # Ex. Regular (ex. Completed) & Custom Lists
        for entries in listType['entries']:
            media: dict = entries['media']
            idAni: int = media['id']
            idMal: int = media['idMal']

            # Check if Anime already in hash table
            if idAni in animelist:
                # Already encountered, must be in a custom list
                # Update custom list then continue to next Anime
                if listType['name'] not in STDLISTS:
                    animelist[idAni].customList.append(listType['name'])
                continue

            # Parse the data
            titles: dict[str: str] = media['title']
            if titles['english'] != None:
                title: str = titles['english']
            else:
                title: str = titles['romaji']
            genres: list[str] = media['genres']
            format: str = media['format']
            animeStatus: str = media['status']
            episodeCount: int = media['episodes']
            countryOfOrigin: str = media['countryOfOrigin']
            userStatus: str = entries['status']
            score = entries['score']
            progress: int = entries['progress']
            repeats: int = entries['repeat']
            startYear: int = entries['startedAt']['year']
            startMonth: int = entries['startedAt']['month']
            startDay: int = entries['startedAt']['day']
            endYear: int = entries['completedAt']['year']
            endMonth: int = entries['completedAt']['month']
            endDay: int = entries['completedAt']['day']
            notes: str = entries['notes']
            if listType['name'] in STDLISTS:
                customList = []
            else:
                customList = [listType['name']]
                # Does not account for Anime in more than one custom list

            # Add the Anime to the hash table
            animelist[idAni] = Anime(idAni, idMal, title, genres, format, 
                                     animeStatus, episodeCount, countryOfOrigin, 
                                     userStatus, score, progress, repeats, 
                                     startYear, startMonth, startDay, endYear, 
                                     endMonth, endDay, notes, customList)

    return animelist

def mangaList(username):
    '''Returns a hash table of a user's manga list. The anime's
    title, genres, format, animeStatus, chapterCount, volumecount,
    countryOfOrigin, userStatus, and score are stored as the value, with the
    anime's title stored as the key
    '''
    mangalist = {}
    variables = create_vars(username)
    response = requests.post(URL, json={'query':query, 'variables':variables})
    response = response.json()    # Turn json into hash table

    data: dict[str: Manga] = response['data']
    manga = data['manga']
    lists = manga['lists']
    for listType in lists:
        for entries in listType['entries']:
            media = entries['media']
            idAni = media['id']
            idMal = media['idMal']
            titles = media['title']
            if titles['english'] != None:
                title = titles['english']
            else:
                title = titles['romaji']
            genres = media['genres']
            format = media['format']
            mangaStatus = media['status']
            chapterCount = media['chapters']
            volumeCount = media['volumes']
            countryOfOrigin = media['countryOfOrigin']
            userStatus = entries['status']
            score = entries['score']
            progress = entries['progress']
            progressVolumes = entries['progressVolumes']
            repeats = entries['repeat']
            startYear = entries['startedAt']['year']
            startMonth = entries['startedAt']['month']
            startDay = entries['startedAt']['day']
            endYear = entries['completedAt']['year']
            endMonth = entries['completedAt']['month']
            endDay = entries['completedAt']['day']
            notes = entries['notes']
            if listType['name'] in STDLISTS:
                customList = None
            else:
                customList = listType['name']
                # Does not account for manga in more than one custom list
            mangalist[title] = Manga(idAni, idMal, title, genres, format, 
                                     mangaStatus, chapterCount, volumeCount, 
                                     countryOfOrigin, userStatus, score, 
                                     progress, progressVolumes, repeats, 
                                     startYear, startMonth, startDay, endYear, 
                                     endMonth, endDay, notes, customList)
    return mangalist

def create_user(username, animeList, mangaList):
    '''Returns a User object'''
    variables = create_vars(username)
    response = requests.post(URL, json={'query':query, 'variables':variables})
    response = response.json()    # Turn json into hash table

    data = response['data']
    user = data['User']
    name = user['name']
    id = user['id']
    statistics = user['statistics']

    anime = statistics['anime']
    animeCount = anime['count']
    animeMeanScore = anime['meanScore']
    animeStandardDeviation = anime['standardDeviation']
    animeMinutesWatched = anime['minutesWatched']
    animeEpisodesWatched = anime['episodesWatched']
    animeGenreList = []
    animeGenres = anime['genres']
    for genreEntry in animeGenres:
        animeGenre = genreEntry['genre']
        animeGenreCount = genreEntry['count']
        animeGenreMeanScore = genreEntry['meanScore']
        animeGenreList.append(Genre(animeGenre, animeGenreCount, animeGenreMeanScore))
    animeTagList = []
    animeTags = anime['tags']
    for tagEntry in animeTags:
        animeTag = tagEntry['tag']['name']
        animeTagCount = tagEntry['count']
        animeTagMeanScore = tagEntry['meanScore']
        animeTagList.append(Tag(animeTag, animeTagCount, animeTagMeanScore))

    manga = statistics['manga']
    mangaCount = manga['count']
    mangaMeanScore = manga['meanScore']
    mangaStandardDeviation = manga['standardDeviation']
    chaptersRead = manga['chaptersRead']
    volumesRead = manga['volumesRead']
    mangaGenreList = []
    mangaGenres = manga['genres']
    for genreEntry in mangaGenres:
        mangaGenre = genreEntry['genre']
        mangaGenreCount = genreEntry['count']
        mangaGenreMeanScore = genreEntry['meanScore']
        mangaGenreList.append(Genre(mangaGenre, mangaGenreCount, mangaGenreMeanScore))
    mangaTagList = []
    mangaTags = manga['tags']
    for tagEntry in mangaTags:
        mangaTag = tagEntry['tag']['name']
        mangaTagCount = tagEntry['count']
        mangaTagMeanScore = tagEntry['meanScore']
        mangaTagList.append(Tag(mangaTag, mangaTagCount, mangaTagMeanScore))

    user = User(name, id, animeList, animeCount, animeMeanScore, 
                animeStandardDeviation, animeMinutesWatched, 
                animeEpisodesWatched, animeGenreList, animeTagList,
                mangaList, mangaCount, mangaMeanScore, mangaStandardDeviation,
                chaptersRead, volumesRead, mangaGenreList, mangaTagList)
    return user

def sort_by_score(dict):
    '''Takes in a dictionary of anime/manga,
       returns a list of Anime/Manga sorted by scores'''
    sorted = OrderedList()
    for media in dict.values():
        sorted.add(media)
    sortedList = sorted.python_list()
    return sortedList

def sort_by_title(ht: dict) -> list:
    '''Takes in a hash table of dict[int: Anime/Manga],
       returns a list of Anime/Manga sorted by titles'''
    titleIdList: list[(str, int)] = []
    for media in ht.values():
        titleIdList.append((media.title, media.idAni))
    titleIdList.sort(key=lambda x: x[0])    # Sort by media title

    ret = []
    for tuple in titleIdList:
        ret.append(ht[tuple[1]])
    return ret

def main(username):
    animelist = animeList(username)
    mangalist = mangaList(username)
    user = create_user(username, animelist, mangalist)

    with open(f"./{username}'s Anime List.txt", "w", encoding='utf-8') as file:
        file.write(f"Total anime count: {len(user.animeList)}\n")
        file.write(f"Total anime excluding planned: {user.animeCount}\n\n")
        for anime in sort_by_title(user.animeList):
            file.write(f"{anime.title}:\n")
            file.write(f"\tAniList ID: {anime.idAni}, MAL ID: {anime.idMal}\n")
            file.write(f"\t{anime.userStatus}\n")
            file.write(f"\tEpisode Progress: {anime.progress}/{anime.episodeCount}\n")
            file.write(f"\tScore: {anime.score}\n")
            file.write(f"\tRewatches: {anime.repeats}\n")
            file.write(f"\t{anime.startDate} - {anime.endDate}\n")
            file.write(f"\tNotes: {anime.notes}\n")
            file.write(f"\tCustom List: {anime.customList}\n")

    with open(f"./{username}'s Manga List.txt", "w", encoding='utf-8') as file:
        file.write(f"Total manga count: {len(user.mangaList)}\n")
        file.write(f"Total manga excluding planned: {user.mangaCount}\n\n")
        for manga in sort_by_title(user.mangaList):
            file.write(f"{manga.title}:\n")
            file.write(f"\tAniList ID: {manga.idAni}, MAL ID: {manga.idMal}\n")
            file.write(f"\t{manga.userStatus}\n")
            file.write(f"\tChapter Progress: {manga.progress}/{manga.chapterCount}\n")
            file.write(f"\tVolume Progress: {manga.progressVolumes}/{manga.volumeCount}\n")
            file.write(f"\tScore: {manga.score}\n")
            file.write(f"\tRereads: {manga.repeats}\n")
            file.write(f"\t{manga.startDate} - {manga.endDate}\n")
            file.write(f"\tNotes: {manga.notes}\n")
            file.write(f"\tCustom List: {manga.customList}\n")

if __name__ == '__main__':
    username = input("AniList Username: ")
    main(username)