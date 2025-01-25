from tkinter import ttk
from service.hangman import HangmanGame, VALID_CHARS
import tkinter as tk
from service.gif_displayer import ImageLabel
import random


MAX_LIVES = 9
GIF_COUNT = 7


class HangmanUI:
    def __init__(self, window):
        self.root = window
        self.root.title("Hangman Game")
        self.root.geometry("1000x600")

        # Initialize the game logic
        self.game = HangmanGame()
        self.lives = 0

        # Dropdown variables
        self.category_var = tk.StringVar()
        self.category_var.set("Select a category")

        # ui Setup
        self.main_frame = tk.Frame(self.root)
        self.left_frame = tk.Frame(self.main_frame, width=300, height=400, padx=10, bg="white")
        self.hangman_image = tk.PhotoImage(file="images/0.png")
        self.hangman_label = tk.Label(self.left_frame, image=self.hangman_image)
        self.gif_label = ImageLabel(self.left_frame)
        self.right_frame = tk.Frame(self.main_frame, width=300, height=400)
        self.title_label = tk.Label(self.right_frame, text="Hangman Game", font=("Arial", 24), fg="blue")
        self.play_button = tk.Button(self.right_frame, text="Start", font=("Arial", 16), command=self.on_start_click)
        self.word_to_guess = tk.Label(self.right_frame, text="", font=("Cascadia Code", 20), wraplength=450)
        self.end_message = tk.Label(self.right_frame, text="", font=("Arial", 16))
        self.letters_frame = tk.Frame(self.right_frame)
        self.letter_buttons = {}
        self.exit_button = tk.Button(self.right_frame, text="Exit", font=("Arial", 16), command=self.root.quit)
        self.combobox = ttk.Combobox(self.right_frame, textvariable=self.category_var, font=("Arial", 14),
                                     state="readonly", width=40)
        self.setup_ui()

    def setup_ui(self):
        # Main frame for layout
        self.main_frame.pack(fill="both", expand=True)

        # Left side for the hangman image
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        # Placeholder for the hangman image
        self.hangman_label.image = self.hangman_image
        self.hangman_label.pack(expand=True)

        # Right side for buttons and game controls
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_propagate(False)

        # Title Label
        self.title_label.pack(pady=20)

        # Combobox setup
        self.combobox["values"] = self.game.categories
        self.combobox.pack(pady=10)

        # Default value
        self.combobox.set("Select a category")

        # Bind selection event
        self.combobox.bind("<<ComboboxSelected>>", self.on_category_selected)

        # Play Button
        self.play_button.pack(pady=10)
        self.play_button.config(state="disabled", disabledforeground="gray")

        # Word to guess display
        self.word_to_guess.pack(pady=10)

        # Word to guess display
        self.end_message.pack(pady=10)

        # Buttons for letters
        self.letters_frame.pack(pady=10)

        for i, letter in enumerate(VALID_CHARS):
            formatted_letter = letter.upper()
            btn = tk.Button(self.letters_frame, state="disabled", text=formatted_letter, width=4, font=("Arial", 12),
                            command=lambda l=formatted_letter: self.on_letter_click(l))
            btn.grid(row=i // 8, column=i % 8, padx=2, pady=2)
            self.letter_buttons[formatted_letter] = btn

        # Exit Button
        self.exit_button.pack(pady=10)

    def on_category_selected(self, event):
        self.play_button.config(state="active")

    def on_start_click(self):
        """Handles the start button click."""
        self.game.start_game(self.category_var.get())
        self.gif_label.forget()
        self.hangman_label.pack()
        self.lives = 0
        self.update_image()
        self.word_to_guess.config(text=self.game.get_display_word())
        self.end_message.config(text="")
        self.reset_letter_buttons()
        self.gif_label = ImageLabel(self.left_frame)
        self.combobox.config(state="disabled")
        self.play_button.config(state="disabled")

    def on_letter_click(self, letter):
        """Handles a letter button click."""
        self.letter_buttons[letter].config(state="disabled", disabledforeground="gray")
        result = self.game.guess_letter(letter)
        if not result.success:
            self.lives += 1
            self.update_image()
        self.word_to_guess.config(text=self.game.get_display_word())
        if self.game.is_winning:
            self.end_game("You won!", False)
        elif self.lives >= MAX_LIVES:
            self.end_game("Game over!", True)

    def update_image(self):
        """Updates the hangman image."""
        new_image = tk.PhotoImage(file=f"images/{self.lives}.png")
        self.hangman_label.config(image=new_image)
        self.hangman_label.image = new_image

    def reset_letter_buttons(self):
        """Resets the letter buttons."""
        for btn in self.letter_buttons.values():
            btn.config(state="normal")

    def get_gif_path(self):
        random_num = random.randint(1, GIF_COUNT)
        if self.game.is_winning:
            return f"images/win{random_num}.gif"
        return f"images/lose{random_num}.gif"

    def show_gif(self):
        path = self.get_gif_path()
        self.hangman_label.pack_forget()
        self.gif_label.load(path)
        self.gif_label.pack(expand=True)

    def end_game(self, message, is_over):
        """Handles the end of the game."""
        self.word_to_guess.config(text=self.game.get_display_word())
        for btn in self.letter_buttons.values():
            btn.config(state="disabled")
        if is_over:
            self.end_message.config(text=f"The word was: {self.game.chosen_word}")
        self.combobox.config(state="readonly")
        self.play_button.config(state="active")
        self.root.after(500, self.show_gif)
