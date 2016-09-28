import logging

import aiohttp
import asyncio
import motor.motor_asyncio

import utils

OMDB_URL = 'https://www.omdbapi.com/'

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


async def get_movie_by_id(session, movie_id):
    imdb_id = utils.generate_imdb_id_from_number(movie_id)
    search_response = await _get_movie_response(session, imdb_id)
    json_movie = await search_response.json()
    return MovieData.from_dict(json_movie)


async def _get_movie_response(session, imdb_id):
    payload = {
        'i': imdb_id, 'plot': 'full', 'r': 'json'
    }
    async with session.get(OMDB_URL, params=payload) as resp:
        return resp


async def insert_movie_into_collection(collection, movie):
    movie_present = await collection.find_one({'imdbid': movie.imdbid})
    if movie_present and movie.imdbid != 'unknown':
        logging.info('Movie is already in the database.')
        return
    else:
        await collection.insert(movie.to_dict())


async def extract_last_movie_id(movie_collection):
    """Find the last movie in the collection,
    extract its consequent number from the IMDB id, and update counter
    if necessary."""
    last_movie = None
    cursor = movie_collection.find().sort('_id', -1).limit(1)

    while (await cursor.fetch_next):
        last_movie = cursor.next_object()

    if last_movie is None:
        return 0
    last_id = utils.extract_id_from_imdbid(last_movie['imdbid'])
    return int(last_id)


async def download_movies_data(loop, collection, counter_collection):
    currently_parsed_movies = await counter_collection.find_one({'name': 'movies'})
    if currently_parsed_movies and currently_parsed_movies != '0':
        currently_parsed_movies = int(currently_parsed_movies['count'])
    else:
        currently_parsed_movies = await extract_last_movie_id(collection)

    await counter_collection.update({'name': 'movies'},
                                    {'count': currently_parsed_movies + 1},
                                    upsert=True)
    async with aiohttp.ClientSession(loop=loop) as session:
        for movie_id in range(currently_parsed_movies,
                              currently_parsed_movies + 1000000):
            try:
                m = await get_movie_by_id(session, movie_id)
                await insert_movie_into_collection(collection, m)

                currently_parsed_movies += 1
                await counter_collection.update({'name': 'movies'},
                                                {'count': currently_parsed_movies},
                                                upsert=True)
            except Exception as e:
                logging.exception("Unknown error occured.")


def main():
    client = motor.motor_asyncio.AsyncIOMotorClient()

    movies_db = client.movies_db
    movies_collection = movies_db.movies_collection
    counter_collection = movies_db.counter

    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_movies_data(loop,
                                                 movies_collection,
                                                 counter_collection))


if __name__ == '__main__':
    main()
