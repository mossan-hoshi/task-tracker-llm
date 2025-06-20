import tkinter as tk


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()

    def _setup_window(self):
        self.root.title("Task Tracker")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

    def start(self):
        self.root.mainloop()
