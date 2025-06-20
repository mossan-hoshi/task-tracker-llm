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


if __name__ == "__main__":
    unittest.main()
