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

        _window = MainWindow(self.root)
        self.assertEqual(self.root.title(), "Task Tracker")

    def test_window_geometry(self):
        from src.gui.main_window import MainWindow

        _window = MainWindow(self.root)
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

        _window = MainWindow(self.root)
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

    def test_session_integration(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        self.assertIsNone(window.current_session)

        window.task_entry.insert(0, "テストタスク")
        window._on_start_clicked()

        self.assertIsNotNone(window.current_session)
        self.assertEqual(window.current_session.task_name, "テストタスク")
        self.assertTrue(window.current_session.is_running)
        self.assertEqual(window.task_entry.get(), "")

    def test_empty_task_name_ignored(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)
        window.task_entry.insert(0, "   ")
        window._on_start_clicked()

        self.assertIsNone(window.current_session)

    def test_session_switching(self):
        from src.gui.main_window import MainWindow

        window = MainWindow(self.root)

        window.task_entry.insert(0, "タスク1")
        window._on_start_clicked()
        first_session = window.current_session

        window.task_entry.insert(0, "タスク2")
        window._on_start_clicked()
        second_session = window.current_session

        self.assertFalse(first_session.is_running)
        self.assertTrue(second_session.is_running)
        self.assertEqual(second_session.task_name, "タスク2")


if __name__ == "__main__":
    unittest.main()
