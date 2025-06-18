from uuid import uuid4
import copy


class FakeSessionRepository():
    def __init__(self, initial_sessions: list = None):
        # Store deep copies of the initial sessions
        self.sessions = []
        if initial_sessions:
            for session in initial_sessions:
                session_copy = copy.deepcopy(session)
                if session_copy.id is None:
                    session_copy.id = uuid4()
                self.sessions.append(session_copy)

    def find_by_id(self, session_id: str):
        """Find a session by its ID"""
        for session in self.sessions:
            if session.id == session_id:
                # Return a deep copy of the found session
                return copy.deepcopy(session)
        return None
        
    def save(self, session):
        """Save a session to the repository"""
        # Make a deep copy before saving
        session_copy = copy.deepcopy(session)
        
        # Generate ID if needed
        if session_copy.id is None:
            session_copy.id = uuid4()
            
        # Check if we need to update an existing session
        for i, existing_session in enumerate(self.sessions):
            if existing_session.id == session_copy.id:
                self.sessions[i] = session_copy
                return session_copy
                
        # Add as a new session
        self.sessions.append(session_copy)
        return session_copy.id