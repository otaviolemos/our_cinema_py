from datetime import datetime, timedelta
from domain.errors import SeatAlreadyReservedError
from domain.room import Room
from domain.session import Session
from domain.user import User
from test.builder.movie_builder import MovieBuilder
from test.doubles.fake_key_value_repository import FakeKeyValueRepository
from test.doubles.fake_reservation_repository import FakeReservationRepository
from test.doubles.fake_session_repository import FakeSessionRepository
from test.doubles.fake_user_repository import FakeUserRepository
from test.doubles.key_value_repository_stub_for_racing_condition import KeyValueRepositoryStubForRacingCondition
from use_cases.reserve_seats import ReserveSeats
import pytest

def test_reserve_available_seats():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)

    registeredUser = User("test_user")
    registeredRoom = Room("1")
    registeredMovie = MovieBuilder().aMovie().build()
    registeredSession = Session(registeredRoom, registeredMovie, tomorrow_at_seven_pm)
    
    emptyReservationRepo = FakeReservationRepository()
    singleUserUserRepository = FakeUserRepository()
    singleSessionSessionRepository = FakeSessionRepository()

    session_id = singleSessionSessionRepository.save(registeredSession)
    user_id = singleUserUserRepository.save(registeredUser)

    keyValueRepository = FakeKeyValueRepository()

    useCase = ReserveSeats(emptyReservationRepo, singleUserUserRepository, singleSessionSessionRepository, keyValueRepository)

    response = useCase.perform(['A1', 'A2'], session_id, user_id)
    assert response.id is not None
    
    reservation_id = response.id
    a1_key_value = f"A1-{session_id}"
    a2_key_value = f"A2-{session_id}"

    assert keyValueRepository.get(a1_key_value) == reservation_id
    assert keyValueRepository.get(a2_key_value) == reservation_id

def test_reserve_temporarily_unavaiable_seats():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)

    registeredUser = User("test_user")
    registeredRoom = Room("1")
    registeredMovie = MovieBuilder().aMovie().build()
    registeredSession = Session(registeredRoom, registeredMovie, tomorrow_at_seven_pm)
    
    emptyReservationRepo = FakeReservationRepository()
    singleUserUserRepository = FakeUserRepository()
    singleSessionSessionRepository = FakeSessionRepository()

    session_id = singleSessionSessionRepository.save(registeredSession)
    user_id = singleUserUserRepository.save(registeredUser)

    keyValueRepository = FakeKeyValueRepository()

    useCase = ReserveSeats(emptyReservationRepo, singleUserUserRepository, singleSessionSessionRepository, keyValueRepository)

    # Reserve A1 and A2
    useCase.perform(['A1', 'A2'], session_id, user_id)

    with pytest.raises(SeatAlreadyReservedError):
        useCase.perform(['A1'], session_id, user_id)

    assert keyValueRepository.get(f"A1-{session_id}") is not None

def test_racing_condition_on_temporary_reservation():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)

    registeredUser = User("test_user")
    registeredRoom = Room("1")
    registeredMovie = MovieBuilder().aMovie().build()
    registeredSession = Session(registeredRoom, registeredMovie, tomorrow_at_seven_pm)
    
    emptyReservationRepo = FakeReservationRepository()
    singleUserUserRepository = FakeUserRepository()
    singleSessionSessionRepository = FakeSessionRepository()

    session_id = singleSessionSessionRepository.save(registeredSession)
    user_id = singleUserUserRepository.save(registeredUser)

    keyValueRepository = KeyValueRepositoryStubForRacingCondition()

    useCase = ReserveSeats(emptyReservationRepo, singleUserUserRepository, singleSessionSessionRepository, keyValueRepository)

    with pytest.raises(SeatAlreadyReservedError):
        useCase.perform(['A1'], session_id, user_id)