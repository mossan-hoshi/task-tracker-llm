from datetime import datetime
from typing import Optional


class Session:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.is_running = False

    def start(self) -> None:
        if self.is_running:
            raise ValueError("Session is already running")
        
        self.start_time = datetime.now()
        self.is_running = True
        self.end_time = None

    def stop(self) -> None:
        if not self.is_running:
            raise ValueError("Session is not running")
        
        self.end_time = datetime.now()
        self.is_running = False

    def get_duration(self) -> float:
        if self.start_time is None:
            return 0.0
        
        end_time = self.end_time if self.end_time else datetime.now()
        delta = end_time - self.start_time
        return delta.total_seconds()

    def format_duration(self) -> str:
        duration = self.get_duration()
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def __str__(self) -> str:
        return f"{self.task_name}: {self.format_duration()}"