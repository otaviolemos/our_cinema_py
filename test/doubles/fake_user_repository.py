from domain.user import User


class FakeUserRepository:
    """An in-memory implementation of the UserRepository protocol for testing"""
    
    def __init__(self, initial_users: list[User] = None):
        self.users = initial_users or []