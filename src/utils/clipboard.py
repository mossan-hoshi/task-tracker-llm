import tkinter as tk


class ClipboardManager:
    def copy_to_clipboard(self, text: str) -> bool:
        try:
            root = tk.Tk()
            root.withdraw()
            
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()
            root.destroy()
            
            return True
        except Exception:
            return False