from domain.user import User
from uuid import uuid4


class FakeUserRepository:
    """An in-memory implementation of the UserRepository protocol for testing"""
    
    def __init__(self, initial_users: list[User] = None):
        initial_users = initial_users or []
        for user in initial_users:
            if user.id is None:
                user.id = uuid4()
        self.users = initial_users
    
    def save(self, user: User) -> None:
        """Save a user to the repository.
        If the user already exists, it will be updated."""
        if user.id is None:
            user.id = uuid4()
            
        for i, existing_user in enumerate(self.users):
            if existing_user.id == user.id:
                self.users[i] = user
                return
        self.users.append(user)
        return user.id
    
    def find_by_id(self, user_id: str) -> User:
        """Find a user by its ID"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def find_by_name(self, name: str) -> User:
        """Find a user by name"""
        for user in self.users:
            if user.name == name:
                return user
        return None
    
    def find_all(self) -> list[User]:
        """Return all users"""
        return self.users