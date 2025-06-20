from typing import Dict, Any, List


class CategoryCalculator:
    def calculate_category_totals(self, gemini_response: Dict[str, Any]) -> Dict[str, Any]:
        if "categories" not in gemini_response:
            raise KeyError("Missing 'categories' key in response")

        processed_categories: List[Dict[str, Any]] = []

        for category in gemini_response["categories"]:
            if "name" not in category or "tasks" not in category:
                raise KeyError("Missing required fields in category")

            category_name = category["name"]
            tasks = category["tasks"]

            for task in tasks:
                if "name" not in task or "duration" not in task:
                    raise KeyError("Missing required fields in task")

            calculated_total = sum(task["duration"] for task in tasks)

            processed_category = {"name": category_name, "tasks": tasks, "total_duration": calculated_total}
            processed_categories.append(processed_category)

        return {"categories": processed_categories}

    def get_total_work_time(self, categorized_data: Dict[str, Any]) -> float:
        if "categories" not in categorized_data:
            return 0.0

        total_time = 0.0
        for category in categorized_data["categories"]:
            if "total_duration" in category:
                total_time += category["total_duration"]

        return total_time
