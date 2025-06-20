import tkinter as tk


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()
        self._create_widgets()

    def _setup_window(self):
        self.root.title("Task Tracker")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

    def _create_widgets(self):
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.pack(pady=10)

        self.start_button = tk.Button(self.root, text="▶ 開始")
        self.start_button.pack(pady=5)

    def start(self):
        self.root.mainloop()
