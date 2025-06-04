from src.domain.model import Movie

class MovieBuilder:
    movie: Movie

    def __init__(self):
        pass

    def aMovie(self):
        self.movie = Movie(title='Die Hard 2', genre='Action', duration=90)
        return self

    def build(self):
        return self.movie
    
    def with_duration(self, duration):
        self.movie.duration = duration
        return self