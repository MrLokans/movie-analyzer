import pytest
from utils import (
    IMDB_MAX_DIGITS,
    generate_imdb_id_from_number,
    extract_id_from_imdbid
)

from parser import movie_from_text


class TestIMDBIDGeneration(object):
    def test_negative_numbers_ignored_by_imdb_generator(self):
        with pytest.raises(ValueError):
            generate_imdb_id_from_number(-1)

    def test_imdb_generator_raises_error_for_way_too_big_number(self):
        with pytest.raises(ValueError):
            generate_imdb_id_from_number(100000000000)

    def test_imdb_generator_raises_error_for_non_number(self):
        with pytest.raises(ValueError):
            generate_imdb_id_from_number('nondigit')

    @pytest.mark.parametrize('value, expected', (
                            ('1', 'tt0000001'),
                            (1, 'tt0000001'),
                            (999999, 'tt0999999')))
    def test_sample_inputs(self, value, expected):
        result = generate_imdb_id_from_number(value)
        assert result == expected


class TestIMDBExtraction(object):

    def test_invalid_length_id_raises_value_error(self):
        sample_id = 'tt' + '1' * (IMDB_MAX_DIGITS + 1)
        with pytest.raises(ValueError):
            extract_id_from_imdbid(sample_id)

    def test_invalid_id_raises_value_error(self):
        sample_id = 'notidstring'
        with pytest.raises(ValueError):
            extract_id_from_imdbid(sample_id)

    @pytest.mark.parametrize('value, expected', (
                            ('tt0000001', '1'),
                            ('tt0999999', '999999'),
                            ('tt9999999', '9999999')))
    def test_sample_inputs(self, value, expected):
        result = extract_id_from_imdbid(value)
        assert result == expected


@pytest.fixture
def page_text():
    with open('test-page.html') as f:
        return f.read()


class TestPageParsing(object):
    def test_correctly_extracts_movie_title(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.title == 'Donnie Darko'

    def test_correctly_extracts_movie_plot(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.plot == 'A troubled teenager is plagued by visions of a large bunny rabbit that manipulates him to commit a series of crimes, after narrowly escaping a bizarre accident.'

    def test_correctly_extracts_movie_year(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.year == '2001'

    def test_correctly_extracts_movie_genres(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.genre == 'Drama, Sci-Fi, Thriller'

    def test_correctly_extracts_movie_metascore(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.metascore == '71'

    def test_correctly_extracts_movie_director(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.director == 'Richard Kelly'

    def test_correctly_extracts_movie_actors(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.actors == 'Jake Gyllenhaal, Holmes Osborne, Maggie Gyllenhaal, Daveigh Chase'

    def test_correctly_extracts_movie_language(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.language == 'English'

    def test_correctly_extracts_movie_country(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.country == 'USA'

    def test_correctly_extracts_movie_runtime(self, page_text):
        m = movie_from_text(page_text, 'tt0000001')
        assert m.runtime == '113 min'
