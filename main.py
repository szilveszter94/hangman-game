import tkinter as tk

from ui.hangman_UI import HangmanUI

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanUI(root)
    root.mainloop()
