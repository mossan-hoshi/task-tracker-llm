import unittest
from datetime import datetime, timedelta
from unittest.mock import patch


class TestMarkdownExporter(unittest.TestCase):
    def test_markdown_exporter_creation(self):
        from src.utils.markdown import MarkdownExporter

        exporter = MarkdownExporter()
        self.assertIsNotNone(exporter)

    def test_export_empty_sessions(self):
        from src.utils.markdown import MarkdownExporter

        exporter = MarkdownExporter()
        markdown = exporter.export_sessions([])
        
        self.assertIsInstance(markdown, str)
        self.assertIn("セッションがありません", markdown)

    def test_export_single_session(self):
        from src.utils.markdown import MarkdownExporter
        from src.session import Session

        session = Session("テストタスク")
        session.start_time = datetime(2024, 1, 1, 10, 0, 0)
        session.end_time = datetime(2024, 1, 1, 11, 30, 0)
        session.is_running = False

        exporter = MarkdownExporter()
        markdown = exporter.export_sessions([session])

        self.assertIn("# 作業セッション記録", markdown)
        self.assertIn("テストタスク", markdown)
        self.assertIn("01:30:00", markdown)
        self.assertIn("10:00:00", markdown)
        self.assertIn("11:30:00", markdown)

    def test_export_multiple_sessions(self):
        from src.utils.markdown import MarkdownExporter
        from src.session import Session

        session1 = Session("タスク1")
        session1.start_time = datetime(2024, 1, 1, 9, 0, 0)
        session1.end_time = datetime(2024, 1, 1, 10, 0, 0)
        session1.is_running = False

        session2 = Session("タスク2")
        session2.start_time = datetime(2024, 1, 1, 10, 30, 0)
        session2.end_time = datetime(2024, 1, 1, 12, 0, 0)
        session2.is_running = False

        exporter = MarkdownExporter()
        markdown = exporter.export_sessions([session1, session2])

        self.assertIn("タスク1", markdown)
        self.assertIn("タスク2", markdown)
        self.assertIn("01:00:00", markdown)
        self.assertIn("01:30:00", markdown)

    def test_export_includes_total_time(self):
        from src.utils.markdown import MarkdownExporter
        from src.session import Session

        session1 = Session("タスク1")
        session1.start_time = datetime(2024, 1, 1, 9, 0, 0)
        session1.end_time = datetime(2024, 1, 1, 10, 0, 0)
        session1.is_running = False

        session2 = Session("タスク2")
        session2.start_time = datetime(2024, 1, 1, 10, 30, 0)
        session2.end_time = datetime(2024, 1, 1, 11, 0, 0)
        session2.is_running = False

        exporter = MarkdownExporter()
        markdown = exporter.export_sessions([session1, session2])

        self.assertIn("合計時間", markdown)
        self.assertIn("01:30:00", markdown)

    def test_export_markdown_format(self):
        from src.utils.markdown import MarkdownExporter
        from src.session import Session

        session = Session("フォーマットテスト")
        session.start_time = datetime(2024, 1, 1, 14, 0, 0)
        session.end_time = datetime(2024, 1, 1, 15, 45, 30)
        session.is_running = False

        exporter = MarkdownExporter()
        markdown = exporter.export_sessions([session])

        lines = markdown.strip().split('\n')
        self.assertTrue(any(line.startswith('# ') for line in lines))
        self.assertTrue(any(line.startswith('## ') for line in lines))
        self.assertTrue(any('|' in line for line in lines))

    def test_export_with_current_datetime(self):
        from src.utils.markdown import MarkdownExporter
        from src.session import Session

        session = Session("時刻テスト")
        session.start_time = datetime(2024, 1, 1, 10, 0, 0)
        session.end_time = datetime(2024, 1, 1, 11, 0, 0)
        session.is_running = False

        with patch('src.utils.markdown.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 6, 20, 15, 30, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

            exporter = MarkdownExporter()
            markdown = exporter.export_sessions([session])

            self.assertIn("2024-06-20 15:30", markdown)

    def test_export_handles_japanese_text(self):
        from src.utils.markdown import MarkdownExporter
        from src.session import Session

        session = Session("日本語タスク名：データベース設計")
        session.start_time = datetime(2024, 1, 1, 10, 0, 0)
        session.end_time = datetime(2024, 1, 1, 11, 0, 0)
        session.is_running = False

        exporter = MarkdownExporter()
        markdown = exporter.export_sessions([session])

        self.assertIn("日本語タスク名：データベース設計", markdown)
        self.assertIsInstance(markdown, str)


if __name__ == "__main__":
    unittest.main()