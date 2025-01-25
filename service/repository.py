import json
import locale
import random

FILE_PATH = "data/database.json"


class WordRepository:
    def __init__(self):
        self.data = {}
        self.get_data()

    def get_data(self):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def get_categories(self):
        categories_list = ["**összes kategória**"]
        for category, words in self.data['categories'].items():
            categories_list.append(category)
        locale.setlocale(locale.LC_ALL, "hu_HU.UTF-8")

        return sorted(categories_list, key=locale.strxfrm)

    def get_random_word_by_category(self, category):
        words = []
        if category == "**összes kategória**":
            categories_list = []
            for category, words in self.data['categories'].items():
                categories_list.append(category)
            random_category = random.choice(categories_list)
            words = self.data['categories'][random_category]
        elif category in self.data['categories']:
            words = self.data['categories'][category]

        if len(words):
            return random.choice(words)
        else:
            return None
