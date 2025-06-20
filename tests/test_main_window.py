import unittest
import tkinter as tk
from unittest.mock import patch


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        if self.root:
            self.root.destroy()

    def test_window_creation(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertIsNotNone(window)
        self.assertEqual(window.root, self.root)

    def test_window_title(self):
        from src.gui.main_window import MainWindow

        MainWindow(self.root)
        self.assertEqual(self.root.title(), "Task Tracker")

    def test_window_geometry(self):
        from src.gui.main_window import MainWindow

        MainWindow(self.root)
        geometry = self.root.geometry()
        self.assertIsNotNone(geometry)
        self.assertEqual(self.root.title(), "Task Tracker")
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)

    @patch("tkinter.Tk.mainloop")
    def test_mainloop_called(self, mock_mainloop):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.start()
        mock_mainloop.assert_called_once()

    def test_window_resizable(self):
        from src.gui.main_window import MainWindow

        MainWindow(self.root)
        self.assertTrue(self.root.resizable()[0])
        self.assertTrue(self.root.resizable()[1])

    def test_task_input_field_exists(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertIsNotNone(window.task_entry)
        self.assertEqual(window.task_entry.winfo_class(), "Entry")

    def test_start_button_exists(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertIsNotNone(window.start_button)
        self.assertEqual(window.start_button.winfo_class(), "Button")
        self.assertEqual(window.start_button["text"], "▶ 開始")

    def test_task_input_accepts_text(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "テストタスク")
        self.assertEqual(window.task_entry.get(), "テストタスク")

    def test_start_button_clickable(self):
        from src.gui.main_window import MainWindow
        from unittest.mock import MagicMock

        window = MainWindow(self.root)
        mock_callback = MagicMock()
        window.start_button.configure(command=mock_callback)
        window.start_button.invoke()
        mock_callback.assert_called_once()

    def test_widgets_packed_correctly(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        children = list(self.root.children.values())
        self.assertGreater(len(children), 0)
        self.assertIn(window.task_entry, children)
        self.assertIn(window.start_button, children)

    def test_session_manager_integration(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertIsNotNone(window.session_manager)
        self.assertEqual(len(window.session_manager.sessions), 0)

        window.task_entry.insert(0, "テストタスク")
        window._on_start_clicked()

        self.assertEqual(len(window.session_manager.sessions), 1)
        current_session = window.session_manager.current_session
        self.assertIsNotNone(current_session)
        self.assertEqual(current_session.task_name, "テストタスク")
        self.assertTrue(current_session.is_running)
        self.assertEqual(window.task_entry.get(), "")

    def test_empty_task_name_ignored(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "   ")
        window._on_start_clicked()

        self.assertEqual(len(window.session_manager.sessions), 0)
        self.assertIsNone(window.session_manager.current_session)

    def test_automatic_session_switching(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)

        window.task_entry.insert(0, "タスク1")
        window._on_start_clicked()
        first_session = window.session_manager.current_session

        window.task_entry.insert(0, "タスク2")
        window._on_start_clicked()
        second_session = window.session_manager.current_session

        self.assertEqual(len(window.session_manager.sessions), 2)
        self.assertFalse(first_session.is_running)
        self.assertTrue(second_session.is_running)
        self.assertEqual(second_session.task_name, "タスク2")
        self.assertIsNotNone(first_session.end_time)

    def test_pause_button_exists(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertIsNotNone(window.pause_button)
        self.assertEqual(window.pause_button.winfo_class(), "Button")
        self.assertEqual(window.pause_button["text"], "⏸ 一時停止")

    def test_pause_button_disabled_when_no_session(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertEqual(window.pause_button["state"], "disabled")

    def test_pause_button_enabled_when_session_running(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "テストタスク")
        window._on_start_clicked()

        self.assertEqual(window.pause_button["state"], "normal")

    def test_pause_button_pauses_current_session(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "テストタスク")
        window._on_start_clicked()
        session = window.session_manager.current_session

        window._on_pause_clicked()

        self.assertTrue(session.is_paused)
        self.assertEqual(window.pause_button["text"], "▶ 再開")

    def test_resume_button_resumes_current_session(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "テストタスク")
        window._on_start_clicked()
        session = window.session_manager.current_session

        window._on_pause_clicked()
        window._on_pause_clicked()

        self.assertFalse(session.is_paused)
        self.assertEqual(window.pause_button["text"], "⏸ 一時停止")

    def test_pause_button_disabled_when_no_current_session(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "テストタスク")
        window._on_start_clicked()
        window.session_manager.stop_current_session()

        window._update_button_states()
        self.assertEqual(window.pause_button["state"], "disabled")

    def test_task_list_exists(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertIsNotNone(window.task_list)
        self.assertEqual(window.task_list.winfo_class(), "Listbox")

    def test_task_list_displays_sessions(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "タスク1")
        window._on_start_clicked()
        
        window.task_entry.insert(0, "タスク2")
        window._on_start_clicked()

        window._update_task_list()
        
        self.assertEqual(window.task_list.size(), 2)
        items = [window.task_list.get(i) for i in range(window.task_list.size())]
        self.assertTrue(any("タスク1" in item for item in items))
        self.assertTrue(any("タスク2" in item for item in items))

    def test_task_list_shows_running_status(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "実行中タスク")
        window._on_start_clicked()

        window._update_task_list()
        
        running_item = window.task_list.get(0)
        self.assertIn("▶", running_item)
        self.assertIn("実行中タスク", running_item)

    def test_task_list_shows_paused_status(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "一時停止タスク")
        window._on_start_clicked()
        window._on_pause_clicked()

        window._update_task_list()
        
        paused_item = window.task_list.get(0)
        self.assertIn("⏸", paused_item)
        self.assertIn("一時停止タスク", paused_item)

    def test_task_list_shows_completed_status(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "完了タスク")
        window._on_start_clicked()
        window.session_manager.stop_current_session()

        window._update_task_list()
        
        completed_item = window.task_list.get(0)
        self.assertNotIn("▶", completed_item)
        self.assertNotIn("⏸", completed_item)
        self.assertIn("完了タスク", completed_item)

    def test_task_list_shows_duration(self):
        from src.gui.main_window import MainWindow
        import time

        window = MainWindow(self.root)
        window.task_entry.insert(0, "時間表示テスト")
        window._on_start_clicked()
        time.sleep(0.1)

        window._update_task_list()
        
        item_text = window.task_list.get(0)
        self.assertRegex(item_text, r"\d{2}:\d{2}:\d{2}")

    def test_real_time_update_timer_starts(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "リアルタイム更新テスト")
        window._on_start_clicked()

        self.assertIsNotNone(window._timer_id)

    def test_real_time_update_timer_stops_when_no_running_sessions(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "タイマー停止テスト")
        window._on_start_clicked()
        window.session_manager.stop_current_session()

        window._update_display()
        self.assertIsNone(window._timer_id)

    def test_stop_button_exists(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertIsNotNone(window.stop_button)
        self.assertEqual(window.stop_button.winfo_class(), "Button")
        self.assertEqual(window.stop_button["text"], "⏹ 停止")

    def test_stop_button_stops_all_sessions(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "タスク1")
        window._on_start_clicked()
        
        window.task_entry.insert(0, "タスク2")
        window._on_start_clicked()

        window._on_stop_clicked()

        self.assertEqual(len(window.session_manager.get_completed_sessions()), 2)
        self.assertIsNone(window.session_manager.current_session)

    def test_stop_button_stops_real_time_timer(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "タイマー停止テスト")
        window._on_start_clicked()
        
        self.assertIsNotNone(window._timer_id)
        
        window._on_stop_clicked()
        
        self.assertIsNone(window._timer_id)

    def test_stop_button_shows_summary_view(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "サマリーテスト")
        window._on_start_clicked()

        window._on_stop_clicked()

        self.assertTrue(window._is_summary_view)

    def test_summary_view_widgets_exist(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "サマリーウィジェットテスト")
        window._on_start_clicked()

        window._on_stop_clicked()

        self.assertIsNotNone(window.summary_label)
        self.assertIsNotNone(window.back_button)
        self.assertEqual(window.back_button["text"], "戻る")

    def test_back_button_returns_to_main_view(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "戻るボタンテスト")
        window._on_start_clicked()

        window._on_stop_clicked()
        self.assertTrue(window._is_summary_view)

        window._on_back_clicked()

        self.assertFalse(window._is_summary_view)

    def test_summary_view_displays_session_data(self):
        from src.gui.main_window import MainWindow
        import time

        window = MainWindow(self.root)
        window.task_entry.insert(0, "データ表示テスト")
        window._on_start_clicked()
        time.sleep(0.1)

        window._on_stop_clicked()

        summary_text = window.summary_label.cget("text")
        self.assertIn("データ表示テスト", summary_text)
        self.assertRegex(summary_text, r"\d{2}:\d{2}:\d{2}")


if __name__ == "__main__":
    unittest.main()
