import tkinter as tk
from src.session_manager import SessionManager


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.session_manager = SessionManager()
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

        self.pause_button = tk.Button(self.root, text="⏸ 一時停止", command=self._on_pause_clicked, state="disabled")
        self.pause_button.pack(pady=5)

    def _on_start_clicked(self):
        task_name = self.task_entry.get().strip()
        if not task_name:
            return

        self.session_manager.start_session(task_name)
        self.task_entry.delete(0, tk.END)
        self._update_button_states()

    def _on_pause_clicked(self):
        if not self.session_manager.current_session:
            return

        current_session = self.session_manager.current_session
        if current_session.is_paused:
            current_session.resume()
            self.pause_button.config(text="⏸ 一時停止")
        else:
            current_session.pause()
            self.pause_button.config(text="▶ 再開")

    def _update_button_states(self):
        if self.session_manager.current_session and self.session_manager.current_session.is_running:
            self.pause_button.config(state="normal")
        else:
            self.pause_button.config(state="disabled")

    def start(self):
        self.root.mainloop()
