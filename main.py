import tkinter as tk
from src.gui.main_window import MainWindow


def main():
    root = tk.Tk()
    app = MainWindow(root)
    app.start()


if __name__ == "__main__":
    main()
