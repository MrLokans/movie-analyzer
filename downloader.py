import requests

OMDB_URL = 'http://www.omdbapi.com/'
IMDB_MAX_DIGITS = 7


class MovieData(object):

    __slots__ = ('title', 'year', 'released', 'runtime', 'genre',
                 'director', 'plot', 'language', 'type', 'metascore')

    def __init__(self, title="", year="", released="",
                 runtime="", genre="", director="", plot="", language="",
                 type="", metascore="", **kwargs):
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

    @classmethod
    def from_dict(cls, d):
        new_d = {k.lower(): v for k, v in d.items()}
        return cls(**new_d)

    def to_dict(self):
        return {s: getattr(self, s) for s in self.__slots__}

    def __repr__(self):
        return "MovieData(title='{}', year='{}')".format(self.title, self.year)


def get_movie_by_id(movie_id):
    imdb_id = generate_imdb_id_from_number(movie_id)
    search_response = _get_movie_response(imdb_id)
    if search_response.status_code == '200':
        return None
    return MovieData.from_dict(search_response.json())


def _get_movie_response(imdb_id):
    return requests.get(OMDB_URL, params={'i': imdb_id, 'plot': 'full',
                                          'r': 'json'})


def generate_imdb_id_from_number(number):
    try:
        int(number)
    except:
        raise ValueError('Provided parameter is not a number')

    if number <= 0 or len(str(number)) > IMDB_MAX_DIGITS:
        raise ValueError('Negative or too big number provided.')

    return 'tt{:0>7}'.format(str(number))


def main():
    for i in range(1, 10):
        m = get_movie_by_id(i)
        print(m)


if __name__ == '__main__':
    main()
