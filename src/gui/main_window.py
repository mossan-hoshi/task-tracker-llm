import tkinter as tk
from src.session_manager import SessionManager


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.session_manager = SessionManager()
        self._timer_id = None
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

        self.task_list = tk.Listbox(self.root, width=80, height=15)
        self.task_list.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def _on_start_clicked(self):
        task_name = self.task_entry.get().strip()
        if not task_name:
            return

        self.session_manager.start_session(task_name)
        self.task_entry.delete(0, tk.END)
        self._update_button_states()
        self._update_task_list()
        self._start_real_time_updates()

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
        
        self._update_task_list()

    def _update_button_states(self):
        if self.session_manager.current_session and self.session_manager.current_session.is_running:
            self.pause_button.config(state="normal")
        else:
            self.pause_button.config(state="disabled")

    def _update_task_list(self):
        self.task_list.delete(0, tk.END)
        
        for session in self.session_manager.get_all_sessions():
            status_icon = ""
            if session.is_running:
                if session.is_paused:
                    status_icon = "⏸"
                else:
                    status_icon = "▶"
            
            item_text = f"{status_icon} {session.task_name}: {session.format_duration()}"
            self.task_list.insert(tk.END, item_text)

    def _start_real_time_updates(self):
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        
        self._timer_id = self.root.after(1000, self._update_display)

    def _update_display(self):
        self._update_task_list()
        
        has_running_sessions = any(session.is_running for session in self.session_manager.get_all_sessions())
        if has_running_sessions:
            self._timer_id = self.root.after(1000, self._update_display)
        else:
            self._timer_id = None

    def start(self):
        self.root.mainloop()
