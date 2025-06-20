from datetime import datetime
from typing import Optional


class Session:
    def __init__(self, task_name: str) -> None:
        self.task_name: str = task_name
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.is_running: bool = False
        self.is_paused: bool = False
        self.pause_time: Optional[datetime] = None
        self.total_pause_duration: float = 0.0

    def start(self) -> None:
        if self.is_running:
            raise ValueError("Session is already running")

        self.start_time = datetime.now()
        self.is_running = True
        self.end_time = None

    def pause(self) -> None:
        if not self.is_running:
            raise ValueError("Session is not running")
        if self.is_paused:
            raise ValueError("Session is already paused")

        self.pause_time = datetime.now()
        self.is_paused = True

    def resume(self) -> None:
        if not self.is_paused:
            raise ValueError("Session is not paused")

        if self.pause_time:
            pause_duration = (datetime.now() - self.pause_time).total_seconds()
            self.total_pause_duration += pause_duration

        self.pause_time = None
        self.is_paused = False

    def stop(self) -> None:
        if not self.is_running:
            raise ValueError("Session is not running")

        if self.is_paused:
            self.resume()

        self.end_time = datetime.now()
        self.is_running = False

    def get_duration(self) -> float:
        if self.start_time is None:
            return 0.0

        end_time = self.end_time if self.end_time else datetime.now()
        total_seconds = (end_time - self.start_time).total_seconds()

        current_pause_duration = 0.0
        if self.is_paused and self.pause_time:
            current_pause_duration = (datetime.now() - self.pause_time).total_seconds()

        return total_seconds - self.total_pause_duration - current_pause_duration

    def format_duration(self) -> str:
        duration = self.get_duration()
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def __str__(self) -> str:
        return f"{self.task_name}: {self.format_duration()}"
