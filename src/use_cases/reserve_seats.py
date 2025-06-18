from domain.reservation import Reservation


class ReserveSeats:

    def __init__(self, reservation_repository, user_repository, session_repository, key_value_repository):
        self.reservation_repository = reservation_repository
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.key_value_repository = key_value_repository

    def perform(self, seats: list[str], session_id: str, user_id: str):
        session = self.session_repository.find_by_id(session_id)

        for seat in seats:
            if self.key_value_repository.get(f"{seat}-{session.id}"):
                session.sessionRoom.reserve_seat(seat)

        user = self.user_repository.find_by_id(user_id)

        reservation = Reservation(seats, session, user)
        self.reservation_repository.save(reservation)

        for seat in seats:
            self.key_value_repository.set(f"{seat}-{session.id}", reservation.id)

        return reservation