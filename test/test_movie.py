from src.domain.model import Movie
from test.builder.movie_builder import MovieBuilder

def test_get_formatted_duration_with_hours_and_minutes():
    movie = MovieBuilder().aMovie().build()
    assert movie.formatted_duration() == '1h30min'

def test_get_formatted_duration_with_hours():
    movie = MovieBuilder().aMovie().with_duration(120).build()
    assert movie.formatted_duration() == '2h'

def test_get_formatted_duration_with_less_than_one_hour():
    movie = MovieBuilder().aMovie().with_duration(30).build()
    assert movie.formatted_duration() == '30min'