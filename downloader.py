import logging

import aiohttp
import asyncio
import motor.motor_asyncio

OMDB_URL = 'https://www.omdbapi.com/'
IMDB_MAX_DIGITS = 7
MAX_CONCURRENT_CONNECTIONS = 10

logging.basicConfig(level=logging.INFO)


class MovieData(object):

    __slots__ = ('title', 'year', 'released', 'runtime', 'genre', 'imdbid',
                 'director', 'plot', 'language', 'type', 'metascore')

    def __init__(self, title="", year="", released="",
                 runtime="", genre="", director="", plot="", language="",
                 type="", metascore="", imdbid="", **kwargs):
        self.title = title
        self.year = year
        self.released = released
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.plot = plot
        self.language = language
        self.type = type
        self.metascore = metascore
        if not imdbid:
            self.imdbid = "unknown"
            logging.info("Unknown imbid for movie: {}".format(str(self)))
        else:
            self.imdbid = imdbid

    @classmethod
    def from_dict(cls, d):
        new_d = {k.lower(): v for k, v in d.items()}
        return cls(**new_d)

    def to_dict(self):
        return {s: getattr(self, s) for s in self.__slots__}

    def __repr__(self):
        s = "MovieData(title='{}', year='{}', imdbid='{}')"
        return s.format(self.title.encode('utf-8').decode('utf-8', errors='replace'),
                        self.year.encode('utf-8').decode('utf-8', errors='replace'),
                        self.imdbid.encode('utf-8').decode('utf-8', errors='replace'))


async def get_movie_by_id(session, movie_id, semaphore):
    # semaphore.acquire()
    imdb_id = generate_imdb_id_from_number(movie_id)
    search_response = await _get_movie_response(session, imdb_id)
    # semaphore.release()
    json_movie = await search_response.json()
    return MovieData.from_dict(json_movie)


async def _get_movie_response(session, imdb_id):
    return await session.get(OMDB_URL, params={'i': imdb_id, 'plot': 'full',
                                               'r': 'json'})


def generate_imdb_id_from_number(number):
    try:
        int(number)
    except:
        raise ValueError('Provided parameter is not a number')

    if number <= 0 or len(str(number)) > IMDB_MAX_DIGITS:
        raise ValueError('Negative or too big number provided: {}'.format(number))

    return 'tt{:0>7}'.format(str(number))


async def insert_movie_into_collection(collection, movie):
    movie_present = await collection.find_one({'imdbid': movie.imdbid})
    if movie_present and movie.imdbid != 'unknown':
        logging.info('Movie is already in the database.')
        return
    else:
        await collection.insert(movie.to_dict())


async def download_movies_data(loop, collection, counter_collection, semaphore):
    currently_parsed_movies = await counter_collection.find_one({'name': 'movies'})
    if currently_parsed_movies and currently_parsed_movies != '0':
        currently_parsed_movies = int(currently_parsed_movies['count'])
        counter_collection.insert({'name': 'movies', 'count': currently_parsed_movies})
    else:
        currently_parsed_movies = await collection.find().count() + 1
        counter_collection.update({'name': 'movies'},
                                  {'count': currently_parsed_movies})

    async with aiohttp.ClientSession(loop=loop) as session:
        for movie_id in range(currently_parsed_movies,
                              currently_parsed_movies + 100):
            m = await get_movie_by_id(session, movie_id, semaphore)
            await insert_movie_into_collection(collection, m)

            currently_parsed_movies += 1
            await counter_collection.update({'name': 'movies'}, {'count': currently_parsed_movies})


def main():
    client = motor.motor_asyncio.AsyncIOMotorClient()

    movies_db = client.movies_db
    movies_collection = movies_db.movies_collection
    counter_collection = movies_db.counter

    loop = asyncio.get_event_loop()
    semaphore = asyncio.Semaphore(value=MAX_CONCURRENT_CONNECTIONS, loop=loop)
    loop.run_until_complete(download_movies_data(loop,
                                                 movies_collection,
                                                 counter_collection,
                                                 semaphore))


if __name__ == '__main__':
    main()
