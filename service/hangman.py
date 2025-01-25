import random

from model.result import Result
from service.repository import WordRepository

VALID_CHARS = "aábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz"


class HangmanGame:
    def __init__(self):
        self.repository = WordRepository()
        self.categories = self.repository.get_categories()
        self.chosen_word = ""
        self.guessed_word = ""
        self.guessed_list = []
        self.is_winning = False

    def start_game(self, category):
        self.guessed_list = []
        self.is_winning = False
        self.chosen_word = self.repository.get_random_word_by_category(category)
        self.guessed_word = ''.join("_" if char in VALID_CHARS else char for char in self.chosen_word)

    def handle_valid_char(self, guessed_char):
        self.guessed_list.append(guessed_char)
        if guessed_char in self.chosen_word:
            self.update_guessed_word(guessed_char)
            return Result(True, "")
        return Result(False, "")

    def update_guessed_word(self, guessed_char):
        self.guessed_word = "".join(
            guessed_char if self.chosen_word[i] == guessed_char else self.guessed_word[i]
            for i in range(len(self.chosen_word))
        )

    def get_display_word(self):
        return "".join(self.guessed_word)

    def validate_letter(self, letter):
        if letter == "" or letter not in VALID_CHARS:
            return Result(False, "The letter is not valid.")
        if letter not in self.guessed_list:
            return self.handle_valid_char(letter)

        return Result(False, f"The letter '{letter}' is already used.")

    def check_is_winning(self):
        if "_" not in self.guessed_word:
            self.is_winning = True

    def guess_letter(self, letter):
        formatted_letter = letter.lower()
        validation_result = self.validate_letter(formatted_letter)
        self.check_is_winning()
        return validation_result
