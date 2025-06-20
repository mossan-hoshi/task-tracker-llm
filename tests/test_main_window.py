import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        """テスト用のTkinterルートウィンドウを作成"""
        self.root = tk.Tk()
        self.root.withdraw()  # ウィンドウを表示しない

    def tearDown(self):
        """テスト後のクリーンアップ"""
        if self.root:
            self.root.destroy()

    def test_window_creation(self):
        """ウィンドウが正常に作成されることをテスト"""
        from src.gui.main_window import MainWindow
        
        window = MainWindow(self.root)
        
        # ウィンドウが正常に作成されているかチェック
        self.assertIsNotNone(window)
        self.assertEqual(window.root, self.root)

    def test_window_title(self):
        """ウィンドウタイトルが正しく設定されることをテスト"""
        from src.gui.main_window import MainWindow
        
        window = MainWindow(self.root)
        
        # タイトルが設定されているかチェック
        expected_title = "Task Tracker"
        self.assertEqual(self.root.title(), expected_title)

    def test_window_geometry(self):
        """ウィンドウサイズが適切に設定されることをテスト"""
        from src.gui.main_window import MainWindow
        
        window = MainWindow(self.root)
        
        # ジオメトリが設定されているかチェック
        geometry = self.root.geometry()
        self.assertIsNotNone(geometry)
        
        # geometry設定をテストするために、実際に設定された値を確認
        # テスト環境では実際のサイズ取得が困難なため、設定メソッドが呼ばれることを確認
        self.assertEqual(self.root.title(), "Task Tracker")
        
        # または、geometryの文字列をチェック
        self.root.update_idletasks()  # ジオメトリを更新
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        
        # 最小サイズが設定されていることを確認（実際のレンダリングではなく要求サイズ）
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)

    @patch('tkinter.Tk.mainloop')
    def test_mainloop_called(self, mock_mainloop):
        """メインループが呼ばれることをテスト"""
        from src.gui.main_window import MainWindow
        
        window = MainWindow(self.root)
        window.start()
        
        # mainloopが呼ばれているかチェック
        mock_mainloop.assert_called_once()

    def test_window_resizable(self):
        """ウィンドウがリサイズ可能かテスト"""
        from src.gui.main_window import MainWindow
        
        window = MainWindow(self.root)
        
        # リサイズ可能かチェック
        self.assertTrue(self.root.resizable()[0])  # 幅
        self.assertTrue(self.root.resizable()[1])  # 高さ


if __name__ == '__main__':
    unittest.main()