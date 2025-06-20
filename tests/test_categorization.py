import unittest
from src.utils.categorization import CategoryCalculator


class TestCategoryCalculator(unittest.TestCase):
    def test_calculate_category_totals_single_category(self) -> None:
        gemini_response = {
            "categories": [
                {
                    "name": "開発",
                    "tasks": [{"name": "API実装", "duration": 3600.0}, {"name": "UI作成", "duration": 1800.0}],
                    "total_duration": 5400.0,
                }
            ]
        }

        calculator = CategoryCalculator()
        result = calculator.calculate_category_totals(gemini_response)

        self.assertIsInstance(result, dict)
        self.assertIn("categories", result)
        self.assertEqual(len(result["categories"]), 1)

        category = result["categories"][0]
        self.assertEqual(category["name"], "開発")
        self.assertEqual(category["total_duration"], 5400.0)
        self.assertEqual(len(category["tasks"]), 2)

    def test_calculate_category_totals_multiple_categories(self) -> None:
        gemini_response = {
            "categories": [
                {"name": "開発", "tasks": [{"name": "コーディング", "duration": 3600.0}], "total_duration": 3600.0},
                {"name": "テスト", "tasks": [{"name": "単体テスト", "duration": 1800.0}], "total_duration": 1800.0},
            ]
        }

        calculator = CategoryCalculator()
        result = calculator.calculate_category_totals(gemini_response)

        self.assertEqual(len(result["categories"]), 2)

        dev_category = next(cat for cat in result["categories"] if cat["name"] == "開発")
        test_category = next(cat for cat in result["categories"] if cat["name"] == "テスト")

        self.assertEqual(dev_category["total_duration"], 3600.0)
        self.assertEqual(test_category["total_duration"], 1800.0)

    def test_calculate_category_totals_validates_duration_sums(self) -> None:
        gemini_response = {
            "categories": [
                {
                    "name": "開発",
                    "tasks": [{"name": "タスク1", "duration": 1000.0}, {"name": "タスク2", "duration": 2000.0}],
                    "total_duration": 2500.0,
                }
            ]
        }

        calculator = CategoryCalculator()
        result = calculator.calculate_category_totals(gemini_response)

        category = result["categories"][0]
        calculated_total = sum(task["duration"] for task in category["tasks"])
        self.assertEqual(category["total_duration"], calculated_total)

    def test_calculate_category_totals_empty_categories(self) -> None:
        gemini_response: dict[str, list] = {"categories": []}

        calculator = CategoryCalculator()
        result = calculator.calculate_category_totals(gemini_response)

        self.assertIsInstance(result, dict)
        self.assertIn("categories", result)
        self.assertEqual(len(result["categories"]), 0)

    def test_calculate_category_totals_japanese_text_support(self) -> None:
        gemini_response = {
            "categories": [
                {
                    "name": "設計・デザイン",
                    "tasks": [{"name": "データベース設計：ユーザーテーブル", "duration": 7200.0}],
                    "total_duration": 7200.0,
                }
            ]
        }

        calculator = CategoryCalculator()
        result = calculator.calculate_category_totals(gemini_response)

        category = result["categories"][0]
        self.assertEqual(category["name"], "設計・デザイン")
        self.assertEqual(category["tasks"][0]["name"], "データベース設計：ユーザーテーブル")

    def test_calculate_category_totals_invalid_input_structure(self) -> None:
        invalid_response = {"invalid": "structure"}

        calculator = CategoryCalculator()

        with self.assertRaises(KeyError):
            calculator.calculate_category_totals(invalid_response)

    def test_calculate_category_totals_missing_required_fields(self) -> None:
        invalid_response = {"categories": [{"name": "開発", "tasks": [{"name": "タスク"}]}]}

        calculator = CategoryCalculator()

        with self.assertRaises(KeyError):
            calculator.calculate_category_totals(invalid_response)

    def test_get_total_work_time_single_category(self) -> None:
        categorized_data = {"categories": [{"name": "開発", "total_duration": 3600.0}]}

        calculator = CategoryCalculator()
        total_time = calculator.get_total_work_time(categorized_data)

        self.assertEqual(total_time, 3600.0)

    def test_get_total_work_time_multiple_categories(self) -> None:
        categorized_data: dict[str, list] = {
            "categories": [
                {"name": "開発", "total_duration": 3600.0},
                {"name": "テスト", "total_duration": 1800.0},
                {"name": "設計", "total_duration": 900.0},
            ]
        }

        calculator = CategoryCalculator()
        total_time = calculator.get_total_work_time(categorized_data)

        self.assertEqual(total_time, 6300.0)

    def test_get_total_work_time_empty_categories(self) -> None:
        categorized_data: dict[str, list] = {"categories": []}

        calculator = CategoryCalculator()
        total_time = calculator.get_total_work_time(categorized_data)

        self.assertEqual(total_time, 0.0)


if __name__ == "__main__":
    unittest.main()
