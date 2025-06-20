import unittest
from unittest.mock import patch, MagicMock


class TestGeminiAPIClient(unittest.TestCase):
    @patch("src.api.gemini.os.getenv")
    def test_gemini_client_creation(self, mock_getenv: MagicMock) -> None:
        from src.api.gemini import GeminiAPIClient

        mock_getenv.return_value = "test-api-key"
        client = GeminiAPIClient()
        self.assertIsNotNone(client)

    @patch("src.api.gemini.os.getenv")
    def test_api_key_loading_from_env(self, mock_getenv: MagicMock) -> None:
        from src.api.gemini import GeminiAPIClient

        mock_getenv.return_value = "test-api-key"
        client = GeminiAPIClient()

        mock_getenv.assert_called_with("GEMINI_API_KEY")
        self.assertEqual(client.api_key, "test-api-key")

    @patch("src.api.gemini.os.getenv")
    def test_missing_api_key_raises_error(self, mock_getenv: MagicMock) -> None:
        from src.api.gemini import GeminiAPIClient

        mock_getenv.return_value = None

        with self.assertRaises(ValueError) as context:
            GeminiAPIClient()

        self.assertIn("GEMINI_API_KEY", str(context.exception))

    def test_categorize_tasks_stub_returns_typed_response(self) -> None:
        from src.api.gemini import GeminiAPIClient
        from src.session import Session

        session1 = Session("データベース設計")
        session2 = Session("UI実装")
        sessions = [session1, session2]

        with patch("src.api.gemini.os.getenv", return_value="test-key"):
            client = GeminiAPIClient()
            result = client.categorize_tasks_stub(sessions)

        self.assertIsInstance(result, dict)
        self.assertIn("categories", result)
        self.assertIsInstance(result["categories"], list)

        for category in result["categories"]:
            self.assertIsInstance(category, dict)
            self.assertIn("name", category)
            self.assertIn("tasks", category)
            self.assertIn("total_duration", category)
            self.assertIsInstance(category["name"], str)
            self.assertIsInstance(category["tasks"], list)
            self.assertIsInstance(category["total_duration"], float)

    def test_categorize_tasks_stub_categorizes_sessions(self) -> None:
        from src.api.gemini import GeminiAPIClient
        from src.session import Session
        from datetime import datetime

        session1 = Session("データベース設計作業")
        session1.start_time = datetime(2024, 1, 1, 10, 0, 0)
        session1.end_time = datetime(2024, 1, 1, 11, 0, 0)
        session1.is_running = False

        session2 = Session("フロントエンド実装")
        session2.start_time = datetime(2024, 1, 1, 14, 0, 0)
        session2.end_time = datetime(2024, 1, 1, 15, 30, 0)
        session2.is_running = False

        with patch("src.api.gemini.os.getenv", return_value="test-key"):
            client = GeminiAPIClient()
            result = client.categorize_tasks_stub([session1, session2])

        self.assertGreater(len(result["categories"]), 0)

        task_names = []
        for category in result["categories"]:
            task_names.extend([task["name"] for task in category["tasks"]])

        self.assertIn("データベース設計作業", task_names)
        self.assertIn("フロントエンド実装", task_names)

    def test_categorize_tasks_stub_calculates_durations(self) -> None:
        from src.api.gemini import GeminiAPIClient
        from src.session import Session
        from datetime import datetime

        session = Session("テスト作業")
        session.start_time = datetime(2024, 1, 1, 10, 0, 0)
        session.end_time = datetime(2024, 1, 1, 12, 0, 0)
        session.is_running = False

        with patch("src.api.gemini.os.getenv", return_value="test-key"):
            client = GeminiAPIClient()
            result = client.categorize_tasks_stub([session])

        total_duration = sum(cat["total_duration"] for cat in result["categories"])
        self.assertAlmostEqual(total_duration, 7200.0, delta=1.0)

    def test_categorize_tasks_stub_empty_sessions(self) -> None:
        from src.api.gemini import GeminiAPIClient

        with patch("src.api.gemini.os.getenv", return_value="test-key"):
            client = GeminiAPIClient()
            result = client.categorize_tasks_stub([])

        self.assertIsInstance(result, dict)
        self.assertIn("categories", result)
        self.assertEqual(len(result["categories"]), 0)

    def test_categorize_tasks_stub_japanese_text_support(self) -> None:
        from src.api.gemini import GeminiAPIClient
        from src.session import Session

        session = Session("データベース設計：ユーザーテーブル作成")

        with patch("src.api.gemini.os.getenv", return_value="test-key"):
            client = GeminiAPIClient()
            result = client.categorize_tasks_stub([session])

        task_names = []
        for category in result["categories"]:
            task_names.extend([task["name"] for task in category["tasks"]])

        self.assertIn("データベース設計：ユーザーテーブル作成", task_names)

    @patch("src.api.gemini.genai.GenerativeModel")
    @patch("src.api.gemini.genai.configure")
    @patch("src.api.gemini.os.getenv")
    def test_categorize_tasks_real_api_success(
        self,
        mock_getenv: MagicMock,
        mock_configure: MagicMock,
        mock_model_class: MagicMock,
    ) -> None:
        from src.api.gemini import GeminiAPIClient
        from src.session import Session

        mock_getenv.return_value = "test-api-key"
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        mock_response = MagicMock()
        mock_response.text = (
            '{"categories": [{"name": "開発", "tasks": '
            '[{"name": "テスト作業", "duration": 3600.0}], "total_duration": 3600.0}]}'
        )
        mock_model.generate_content.return_value = mock_response

        session = Session("テスト作業")
        client = GeminiAPIClient()
        result = client.categorize_tasks([session])

        self.assertIsInstance(result, dict)
        self.assertIn("categories", result)
        mock_configure.assert_called_once_with(api_key="test-api-key")

    @patch("src.api.gemini.genai.GenerativeModel")
    @patch("src.api.gemini.genai.configure")
    @patch("src.api.gemini.os.getenv")
    def test_categorize_tasks_real_api_error_handling(
        self,
        mock_getenv: MagicMock,
        mock_configure: MagicMock,
        mock_model_class: MagicMock,
    ) -> None:
        from src.api.gemini import GeminiAPIClient
        from src.session import Session

        mock_getenv.return_value = "test-api-key"
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.side_effect = Exception("API Error")

        session = Session("テスト作業")
        client = GeminiAPIClient()

        with self.assertRaises(Exception):
            client.categorize_tasks([session])

    @patch("src.api.gemini.genai.GenerativeModel")
    @patch("src.api.gemini.genai.configure")
    @patch("src.api.gemini.os.getenv")
    def test_categorize_tasks_real_api_invalid_json_response(
        self,
        mock_getenv: MagicMock,
        mock_configure: MagicMock,
        mock_model_class: MagicMock,
    ) -> None:
        from src.api.gemini import GeminiAPIClient
        from src.session import Session

        mock_getenv.return_value = "test-api-key"
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        mock_response = MagicMock()
        mock_response.text = "invalid json"
        mock_model.generate_content.return_value = mock_response

        session = Session("テスト作業")
        client = GeminiAPIClient()

        with self.assertRaises(Exception):
            client.categorize_tasks([session])


if __name__ == "__main__":
    unittest.main()
