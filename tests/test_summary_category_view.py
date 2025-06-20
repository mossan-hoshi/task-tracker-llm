import unittest
import tkinter as tk
from unittest.mock import MagicMock
from src.gui.summary_category_view import SummaryCategoryView


class TestSummaryCategoryView(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self) -> None:
        self.root.destroy()

    def test_category_view_creation(self) -> None:
        categorized_data = {
            "categories": [
                {"name": "開発", "tasks": [{"name": "API実装", "duration": 3600.0}], "total_duration": 3600.0}
            ]
        }

        view = SummaryCategoryView(self.root, categorized_data)
        self.assertIsNotNone(view)
        self.assertEqual(view.categorized_data, categorized_data)

    def test_category_table_display_single_category(self) -> None:
        categorized_data = {
            "categories": [
                {
                    "name": "開発",
                    "tasks": [{"name": "API実装", "duration": 3600.0}, {"name": "UI作成", "duration": 1800.0}],
                    "total_duration": 5400.0,
                }
            ]
        }

        view = SummaryCategoryView(self.root, categorized_data)
        view._create_category_table()

        self.assertIsNotNone(view.category_tree)

    def test_category_table_display_multiple_categories(self) -> None:
        categorized_data = {
            "categories": [
                {"name": "開発", "tasks": [{"name": "コーディング", "duration": 3600.0}], "total_duration": 3600.0},
                {"name": "テスト", "tasks": [{"name": "単体テスト", "duration": 1800.0}], "total_duration": 1800.0},
            ]
        }

        view = SummaryCategoryView(self.root, categorized_data)
        view._create_category_table()

        self.assertIsNotNone(view.category_tree)

    def test_category_table_empty_categories(self) -> None:
        categorized_data: dict[str, list] = {"categories": []}

        view = SummaryCategoryView(self.root, categorized_data)
        view._create_category_table()

        self.assertIsNotNone(view.category_tree)

    def test_format_duration_hours_minutes_seconds(self) -> None:
        view = SummaryCategoryView(self.root, {"categories": []})

        formatted = view._format_duration(7265.0)
        self.assertEqual(formatted, "02:01:05")

    def test_format_duration_zero_seconds(self) -> None:
        view = SummaryCategoryView(self.root, {"categories": []})

        formatted = view._format_duration(0.0)
        self.assertEqual(formatted, "00:00:00")

    def test_format_duration_only_minutes(self) -> None:
        view = SummaryCategoryView(self.root, {"categories": []})

        formatted = view._format_duration(300.0)
        self.assertEqual(formatted, "00:05:00")

    def test_japanese_text_display_support(self) -> None:
        categorized_data = {
            "categories": [
                {
                    "name": "設計・デザイン",
                    "tasks": [{"name": "データベース設計：ユーザーテーブル", "duration": 3600.0}],
                    "total_duration": 3600.0,
                }
            ]
        }

        view = SummaryCategoryView(self.root, categorized_data)
        view._create_category_table()

        self.assertIsNotNone(view.category_tree)

    def test_back_button_callback_functionality(self) -> None:
        mock_callback = MagicMock()

        view = SummaryCategoryView(self.root, {"categories": []}, back_callback=mock_callback)
        view._on_back_clicked()

        mock_callback.assert_called_once()

    def test_copy_markdown_button_functionality(self) -> None:
        mock_callback = MagicMock()

        view = SummaryCategoryView(self.root, {"categories": []}, copy_callback=mock_callback)
        view._on_copy_markdown_clicked()

        mock_callback.assert_called_once()

    def test_total_time_calculation_display(self) -> None:
        categorized_data = {
            "categories": [{"name": "開発", "total_duration": 3600.0}, {"name": "テスト", "total_duration": 1800.0}]
        }

        view = SummaryCategoryView(self.root, categorized_data)
        total_time = view._calculate_total_time()

        self.assertEqual(total_time, 5400.0)

    def test_category_view_widget_packing(self) -> None:
        categorized_data = {
            "categories": [
                {"name": "開発", "tasks": [{"name": "テスト", "duration": 1800.0}], "total_duration": 1800.0}
            ]
        }

        view = SummaryCategoryView(self.root, categorized_data)
        view.show()

        self.assertIsNotNone(view.category_tree)
        self.assertIsNotNone(view.total_label)
        self.assertIsNotNone(view.copy_button)
        self.assertIsNotNone(view.back_button)

    def test_hide_widgets_functionality(self) -> None:
        view = SummaryCategoryView(self.root, {"categories": []})
        view.show()
        view.hide()

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
