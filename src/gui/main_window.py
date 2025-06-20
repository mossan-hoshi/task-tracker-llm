import tkinter as tk
from src.session import Session
from typing import Optional


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.current_session: Optional[Session] = None
        self._setup_window()
        self._create_widgets()

    def _setup_window(self):
        self.root.title("Task Tracker")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

    def _create_widgets(self):
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.pack(pady=10)

        self.start_button = tk.Button(self.root, text="▶ 開始", command=self._on_start_clicked)
        self.start_button.pack(pady=5)

    def _on_start_clicked(self):
        task_name = self.task_entry.get().strip()
        if not task_name:
            return

        if self.current_session:
            self.current_session.stop()

        self.current_session = Session(task_name)
        self.current_session.start()
        self.task_entry.delete(0, tk.END)

    def start(self):
        self.root.mainloop()
