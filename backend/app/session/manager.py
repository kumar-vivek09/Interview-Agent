from app.models.interview import InterviewState
from typing import Dict, Optional

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, InterviewState] = {}
        
    def get_session(self, session_id: str) -> Optional[InterviewState]:
        return self.sessions.get(session_id)
        
    def create_session(self, session_id: str, state: InterviewState):
        self.sessions[session_id] = state
        
    def update_session(self, session_id: str, state: InterviewState):
        self.sessions[session_id] = state

session_manager = SessionManager()
