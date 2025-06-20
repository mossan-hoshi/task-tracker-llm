import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Callable


class SummaryCategoryView:
    def __init__(
        self,
        root: tk.Tk,
        categorized_data: Dict[str, Any],
        back_callback: Optional[Callable[[], None]] = None,
        copy_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        self.root: tk.Tk = root
        self.categorized_data: Dict[str, Any] = categorized_data
        self.back_callback: Optional[Callable[[], None]] = back_callback
        self.copy_callback: Optional[Callable[[], None]] = copy_callback

        self.category_tree: ttk.Treeview
        self.total_label: tk.Label
        self.copy_button: tk.Button
        self.back_button: tk.Button

        self._create_widgets()

    def _create_widgets(self) -> None:
        self._create_category_table()
        self._create_total_label()
        self._create_buttons()

    def _create_category_table(self) -> None:
        columns = ("category", "tasks", "duration")
        self.category_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)

        self.category_tree.heading("category", text="カテゴリ")
        self.category_tree.heading("tasks", text="タスク数")
        self.category_tree.heading("duration", text="合計時間")

        self.category_tree.column("category", width=200, anchor="w")
        self.category_tree.column("tasks", width=100, anchor="center")
        self.category_tree.column("duration", width=120, anchor="e")

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scrollbar.set)

        self._populate_category_table()

    def _populate_category_table(self) -> None:
        categories = self.categorized_data.get("categories", [])

        for category in categories:
            category_name = category.get("name", "")
            tasks = category.get("tasks", [])
            total_duration = category.get("total_duration", 0.0)

            task_count = len(tasks)
            formatted_duration = self._format_duration(total_duration)

            category_item = self.category_tree.insert(
                "", "end", values=(category_name, f"{task_count}個", formatted_duration)
            )

            for task in tasks:
                task_name = task.get("name", "")
                task_duration = task.get("duration", 0.0)
                task_formatted_duration = self._format_duration(task_duration)

                self.category_tree.insert(category_item, "end", values=(f"  {task_name}", "", task_formatted_duration))

    def _create_total_label(self) -> None:
        total_time = self._calculate_total_time()
        formatted_total = self._format_duration(total_time)

        self.total_label = tk.Label(self.root, text=f"総作業時間: {formatted_total}", font=("Arial", 12, "bold"))

    def _create_buttons(self) -> None:
        self.copy_button = tk.Button(self.root, text="Copy Markdown", command=self._on_copy_markdown_clicked, width=15)

        self.back_button = tk.Button(self.root, text="戻る", command=self._on_back_clicked, width=15)

    def _format_duration(self, duration_seconds: float) -> str:
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _calculate_total_time(self) -> float:
        total_time = 0.0
        categories = self.categorized_data.get("categories", [])

        for category in categories:
            total_time += category.get("total_duration", 0.0)

        return total_time

    def _on_back_clicked(self) -> None:
        if self.back_callback:
            self.back_callback()

    def _on_copy_markdown_clicked(self) -> None:
        if self.copy_callback:
            self.copy_callback()

    def show(self) -> None:
        self.category_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.category_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.category_tree.configure(yscrollcommand=scrollbar.set)

        self.total_label.pack(pady=10)
        self.copy_button.pack(pady=5)
        self.back_button.pack(pady=10)

    def hide(self) -> None:
        self.category_tree.pack_forget()
        self.total_label.pack_forget()
        self.copy_button.pack_forget()
        self.back_button.pack_forget()
