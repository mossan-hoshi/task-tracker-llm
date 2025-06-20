import tkinter as tk
from typing import Optional
from src.session_manager import SessionManager
from src.utils.clipboard import ClipboardManager
from src.utils.markdown import MarkdownExporter


class MainWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.session_manager: SessionManager = SessionManager()
        self.clipboard_manager: ClipboardManager = ClipboardManager()
        self.markdown_exporter: MarkdownExporter = MarkdownExporter()
        self._timer_id: Optional[str] = None
        self._is_summary_view: bool = False
        self.task_entry: tk.Entry
        self.start_button: tk.Button
        self.pause_button: tk.Button
        self.stop_button: tk.Button
        self.task_list: tk.Listbox
        self.summary_label: tk.Label
        self.copy_button: tk.Button
        self.back_button: tk.Button
        self._setup_window()
        self._create_widgets()
        self._create_summary_widgets()

    def _setup_window(self) -> None:
        self.root.title("Task Tracker")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

    def _create_widgets(self) -> None:
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.pack(pady=10)

        self.start_button = tk.Button(self.root, text="▶ 開始", command=self._on_start_clicked)
        self.start_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="⏸ 一時停止", command=self._on_pause_clicked, state="disabled")
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="⏹ 停止", command=self._on_stop_clicked)
        self.stop_button.pack(pady=5)

        self.task_list = tk.Listbox(self.root, width=80, height=15)
        self.task_list.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def _on_start_clicked(self) -> None:
        task_name = self.task_entry.get().strip()
        if not task_name:
            return

        self.session_manager.start_session(task_name)
        self.task_entry.delete(0, tk.END)
        self._update_button_states()
        self._update_task_list()
        self._start_real_time_updates()

    def _on_pause_clicked(self) -> None:
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

    def _update_button_states(self) -> None:
        if self.session_manager.current_session and self.session_manager.current_session.is_running:
            self.pause_button.config(state="normal")
        else:
            self.pause_button.config(state="disabled")

    def _update_task_list(self) -> None:
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

    def _start_real_time_updates(self) -> None:
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        
        self._timer_id = self.root.after(1000, self._update_display)

    def _update_display(self) -> None:
        self._update_task_list()
        
        has_running_sessions = any(session.is_running for session in self.session_manager.get_all_sessions())
        if has_running_sessions:
            self._timer_id = self.root.after(1000, self._update_display)
        else:
            self._timer_id = None

    def _on_stop_clicked(self) -> None:
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        
        self.session_manager.stop_all_sessions()
        self._show_summary_view()

    def _create_summary_widgets(self) -> None:
        self.summary_label = tk.Label(self.root, text="", justify=tk.LEFT, anchor="nw")
        self.copy_button = tk.Button(self.root, text="Copy Markdown", command=self._on_copy_markdown_clicked)
        self.back_button = tk.Button(self.root, text="戻る", command=self._on_back_clicked)

    def _show_summary_view(self) -> None:
        self._is_summary_view = True
        
        self.task_entry.pack_forget()
        self.start_button.pack_forget()
        self.pause_button.pack_forget()
        self.stop_button.pack_forget()
        self.task_list.pack_forget()
        
        summary_text = self._generate_summary_text()
        self.summary_label.config(text=summary_text)
        self.summary_label.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.copy_button.pack(pady=5)
        self.back_button.pack(pady=10)

    def _show_main_view(self) -> None:
        self._is_summary_view = False
        
        self.summary_label.pack_forget()
        self.copy_button.pack_forget()
        self.back_button.pack_forget()
        
        self.task_entry.pack(pady=10)
        self.start_button.pack(pady=5)
        self.pause_button.pack(pady=5)
        self.stop_button.pack(pady=5)
        self.task_list.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def _on_back_clicked(self) -> None:
        self._show_main_view()

    def _on_copy_markdown_clicked(self) -> None:
        markdown_text = self.markdown_exporter.export_sessions(self.session_manager.get_all_sessions())
        
        if self.clipboard_manager.copy_to_clipboard(markdown_text):
            original_text = self.copy_button.cget("text")
            self.copy_button.config(text="✓ コピー完了!")
            self.root.after(2000, lambda: self.copy_button.config(text=original_text))
        else:
            original_text = self.copy_button.cget("text")
            self.copy_button.config(text="✗ コピー失敗")
            self.root.after(2000, lambda: self.copy_button.config(text=original_text))

    def _generate_summary_text(self) -> str:
        if not self.session_manager.sessions:
            return "セッションがありません。"
        
        summary_lines = ["作業セッション一覧:\n"]
        for i, session in enumerate(self.session_manager.sessions, 1):
            summary_lines.append(f"{i}. {session.task_name}: {session.format_duration()}")
        
        total_time = self.session_manager.get_total_time()
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        total_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        summary_lines.append(f"\n合計時間: {total_formatted}")
        return "\n".join(summary_lines)

    def start(self) -> None:
        self.root.mainloop()

