import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
from src.session import Session

load_dotenv()


class TaskItem(BaseModel):
    name: str
    duration: float


class CategoryItem(BaseModel):
    name: str
    tasks: List[TaskItem]
    total_duration: float


class CategorizationResponse(BaseModel):
    categories: List[CategoryItem]


class GeminiAPIClient:
    def __init__(self) -> None:
        self.api_key: str = self._load_api_key()
        self.model_name: str = self._load_model_name()
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def _load_api_key(self) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return api_key

    def _load_model_name(self) -> str:
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        return model_name

    def categorize_tasks_stub(self, sessions: List[Session]) -> Dict[str, Any]:
        if not sessions:
            return {"categories": []}

        categories: List[Dict[str, Any]] = []

        development_tasks: List[Dict[str, Any]] = []
        design_tasks: List[Dict[str, Any]] = []
        testing_tasks: List[Dict[str, Any]] = []
        other_tasks: List[Dict[str, Any]] = []

        for session in sessions:
            task_data = {"name": session.task_name, "duration": session.get_duration()}

            task_name_lower = session.task_name.lower()
            if any(
                keyword in task_name_lower
                for keyword in [
                    "実装",
                    "コード",
                    "プログラミング",
                    "開発",
                    "バグ修正",
                    "フロントエンド",
                    "バックエンド",
                ]
            ):
                development_tasks.append(task_data)
            elif any(keyword in task_name_lower for keyword in ["設計", "デザイン", "UI", "UX", "画面", "レイアウト"]):
                design_tasks.append(task_data)
            elif any(keyword in task_name_lower for keyword in ["テスト", "検証", "確認", "デバッグ"]):
                testing_tasks.append(task_data)
            else:
                other_tasks.append(task_data)

        if development_tasks:
            categories.append(
                {
                    "name": "開発",
                    "tasks": development_tasks,
                    "total_duration": sum(task["duration"] for task in development_tasks),
                }
            )

        if design_tasks:
            categories.append(
                {
                    "name": "設計・デザイン",
                    "tasks": design_tasks,
                    "total_duration": sum(task["duration"] for task in design_tasks),
                }
            )

        if testing_tasks:
            categories.append(
                {
                    "name": "テスト・検証",
                    "tasks": testing_tasks,
                    "total_duration": sum(task["duration"] for task in testing_tasks),
                }
            )

        if other_tasks:
            categories.append(
                {
                    "name": "その他",
                    "tasks": other_tasks,
                    "total_duration": sum(task["duration"] for task in other_tasks),
                }
            )

        return {"categories": categories}

    def categorize_tasks(self, sessions: List[Session]) -> Dict[str, Any]:
        if not sessions:
            return {"categories": []}

        tasks_data = []
        for session in sessions:
            tasks_data.append({"name": session.task_name, "duration": session.get_duration()})

        prompt = f"""
以下のタスクリストを作業カテゴリに分類し、カテゴリごとの合計時間を計算してください。

タスクリスト:
{json.dumps(tasks_data, ensure_ascii=False, indent=2)}

可能なカテゴリ例: 開発, 設計・デザイン, テスト・検証, ミーティング, ドキュメント作成, その他

各カテゴリのtotal_durationは、そのカテゴリに属するタスクのduration合計値を設定してください。
"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", response_schema=CategorizationResponse
                ),
            )
            result = json.loads(response.text)
            return result
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from Gemini API: {e}")
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")
