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
            raise ValueError("Can not create movie without imdbid")
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