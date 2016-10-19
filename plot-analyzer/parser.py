import re
from collections import defaultdict

RE_TITLE = r'^MV:\s*(?P<title>[^\n]+)\s+(\((?P<year>\d+)\))'
RE_TITLE = re.compile(RE_TITLE, re.MULTILINE)
SPLITTER = "-------------------------------------------------------------------------------"

fname = "plot.list"


def itersplit(s, sep=None):
    exp = re.compile(r'\s+' if sep is None else re.escape(sep))
    pos = 0
    while True:
        m = exp.search(s, pos)
        if not m:
            if pos < len(s) or sep is not None:
                yield s[pos:]
            break
        if pos < m.start() or sep is not None:
            yield s[pos:m.start()]
        pos = m.end()


def parse_movie_header(header_line: str):
    """Parses header string and extracts
    movie title, year and episode if present
    """
    match = RE_TITLE.match(header_line)
    if match is None:
        msg = "Title {} does not match".format(header_line)
        raise ValueError(msg)
    g = match.groupdict()
    title = g['title']
    year = g['year']
    episode = ""
    return title, year, episode


def parse_plot_lines(plot_lines):
    result = []
    plot = []
    by = ""
    for i, line in enumerate(plot_lines):
        if line.startswith("PL:"):
            plot.append(line.lstrip("PL:"))
        elif line.startswith("BY: "):
            by = line.lstrip("BY: ")
            break

    return [{"text": "".join(plot).strip(), "by": by}]


def get_plot():
    pass


def parse_movie(s: str) -> dict:
    s = s.strip('\n')
    lines = s.split('\n')
    header_line = lines[0]
    plot_lines = lines[1:]

    match = RE_TITLE.match(header_line)
    if match is None:
        msg = "Title {} does not match".format(header_line)
        raise ValueError(msg)
    g = match.groupdict()
    title = g['title']
    year = g['year']
    return {'title': title, 'year': year, 'episode': '',
            'plots': parse_plot_lines(plot_lines)}


data = ""
with open(fname, "r", encoding="latin-1") as f:
    data = f.read()

# for r in RE_TITLE.finditer(data):
#     print(r.groupdict())


def main():
    for n, movie_chunk in enumerate(itersplit(data, sep=SPLITTER)):
        # Skip header
        if n == 0:
            continue
        if n > 500:
            break
        movie_data = parse_movie(movie_chunk)
        print(movie_data)
        print("*" * 10)


if __name__ == '__main__':
    main()
