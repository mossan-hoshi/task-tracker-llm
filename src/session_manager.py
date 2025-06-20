from typing import List, Optional
from src.session import Session


class SessionManager:
    def __init__(self):
        self.sessions: List[Session] = []
        self.current_session: Optional[Session] = None

    def start_session(self, task_name: str) -> Session:
        if self.current_session and self.current_session.is_running:
            self.current_session.stop()

        new_session = Session(task_name)
        new_session.start()
        self.sessions.append(new_session)
        self.current_session = new_session
        return new_session

    def stop_current_session(self) -> None:
        if self.current_session and self.current_session.is_running:
            self.current_session.stop()
            self.current_session = None

    def get_all_sessions(self) -> List[Session]:
        return self.sessions.copy()

    def get_completed_sessions(self) -> List[Session]:
        return [session for session in self.sessions if not session.is_running]

    def get_total_time(self) -> float:
        return sum(session.get_duration() for session in self.sessions)

    def stop_all_sessions(self) -> None:
        if self.current_session and self.current_session.is_running:
            self.current_session.stop()
        self.current_session = None