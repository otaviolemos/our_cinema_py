from datetime import datetime, timedelta
from domain.movie import Movie
from domain.room import Room
from domain.session import Session
from domain.user import User
from test.builder.movie_builder import MovieBuilder
from test.doubles.fake_reservation_repository import FakeReservationRepository
from test.doubles.fake_user_repository import FakeUserRepository


def test_reserve_available_seats():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)

    # user, session, reservation
    registeredUser = User("test_user")
    registeredRoom = Room("1")
    registeredMovie = MovieBuilder.aMovie().build()
    registeredSession = Session(registeredRoom, registeredMovie, tomorrow_at_seven_pm)
    emptyReservationRepo = FakeReservationRepository()
    singleUserUserRepository = FakeUserRepository(registeredUser)

    useCase = ReserveSeats(emptyReservationRepo, singleUserUserRepository, ...)

    response = useCase.perform(['A1', 'A2'], registeredSession.id, registeredUser.id)
    assert response.id is not None

