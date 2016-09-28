import pytest
from utils import (
    IMDB_MAX_DIGITS,
    generate_imdb_id_from_number,
    extract_id_from_imdbid
)


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
