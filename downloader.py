class MovieData(object):

    __slots__ = ('title', 'year', 'released', 'runtime', 'genre',
                 'director', 'plot', 'language', 'type', 'metascore')

    def __init__(self, title="", year="", released="",
                 runtime="", genre="", director="", plot="", language="",
                 type="", metascore=""):
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

    def __repr__(self):
        return "MovieData(title='{}', year='{}')".format(self.title, self.year)
