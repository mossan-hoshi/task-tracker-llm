import unittest
from unittest.mock import patch, MagicMock


class TestClipboardManager(unittest.TestCase):
    def test_clipboard_manager_creation(self):
        from src.utils.clipboard import ClipboardManager

        manager = ClipboardManager()
        self.assertIsNotNone(manager)

    @patch('tkinter.Tk')
    def test_copy_to_clipboard_success(self, mock_tk):
        from src.utils.clipboard import ClipboardManager

        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        manager = ClipboardManager()
        test_text = "# テストMarkdown\n\nテスト内容です。"
        
        result = manager.copy_to_clipboard(test_text)
        
        self.assertTrue(result)
        mock_root.clipboard_clear.assert_called_once()
        mock_root.clipboard_append.assert_called_once_with(test_text)
        mock_root.update.assert_called_once()
        mock_root.destroy.assert_called_once()

    @patch('tkinter.Tk')
    def test_copy_empty_string(self, mock_tk):
        from src.utils.clipboard import ClipboardManager

        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        manager = ClipboardManager()
        
        result = manager.copy_to_clipboard("")
        
        self.assertTrue(result)
        mock_root.clipboard_clear.assert_called_once()
        mock_root.clipboard_append.assert_called_once_with("")

    @patch('tkinter.Tk')
    def test_copy_multiline_text(self, mock_tk):
        from src.utils.clipboard import ClipboardManager

        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        manager = ClipboardManager()
        multiline_text = """# 作業セッション記録

## セッション一覧

| # | タスク名 | 経過時間 |
|---|---|---|
| 1 | テストタスク | 01:30:00 |

## サマリー

**合計時間:** 01:30:00"""
        
        result = manager.copy_to_clipboard(multiline_text)
        
        self.assertTrue(result)
        mock_root.clipboard_append.assert_called_once_with(multiline_text)

    @patch('tkinter.Tk')
    def test_copy_japanese_text(self, mock_tk):
        from src.utils.clipboard import ClipboardManager

        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        manager = ClipboardManager()
        japanese_text = "日本語のテキスト：データベース設計作業"
        
        result = manager.copy_to_clipboard(japanese_text)
        
        self.assertTrue(result)
        mock_root.clipboard_append.assert_called_once_with(japanese_text)

    @patch('tkinter.Tk')
    def test_copy_handles_exception(self, mock_tk):
        from src.utils.clipboard import ClipboardManager

        mock_root = MagicMock()
        mock_root.clipboard_append.side_effect = Exception("クリップボードエラー")
        mock_tk.return_value = mock_root

        manager = ClipboardManager()
        
        result = manager.copy_to_clipboard("テストテキスト")
        
        self.assertFalse(result)

    def test_clipboard_manager_singleton_behavior(self):
        from src.utils.clipboard import ClipboardManager

        manager1 = ClipboardManager()
        manager2 = ClipboardManager()
        
        self.assertIsInstance(manager1, ClipboardManager)
        self.assertIsInstance(manager2, ClipboardManager)


if __name__ == "__main__":
    unittest.main()