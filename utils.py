import re

IMDB_MAX_DIGITS = 7
IMDB_ID_LENGTH = 9
IMDB_REGEX = re.compile(r"tt[0]*(?P<id>\d+)")


def generate_imdb_id_from_number(number):
    try:
        number = int(number)
    except:
        raise ValueError('Provided parameter is not a number')

    if number <= 0 or len(str(number)) > IMDB_MAX_DIGITS:
        msg = 'Negative or too big number provided: {}'
        raise ValueError(msg.format(number))

    return 'tt{:0>7}'.format(str(number))


def extract_id_from_imdbid(imdbid):
    """
    :param imdbid: IMBDB-formatted id
    :type imdbid: str or unicode
    :rtype: str
    >>> number = extract_id_from_imdbid("tt0002996")
    >>> assert number == "2996"
    """
    if len(imdbid) != IMDB_ID_LENGTH or not IMDB_REGEX.match(imdbid):
        raise ValueError("Incorrect IMDB ID: {}".format(imdbid))
    return IMDB_REGEX.match(imdbid).groupdict()['id']
