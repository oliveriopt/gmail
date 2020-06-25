from src.read import TakeEmail
from src.transform import TransformData

import src.variables as var
import json
import ast


class Categories():

    def __init__(self, df):
        self.categories = None
        self.index_categories = None
        self.outcome = df

    def read_categories(self):
        file = open(var.path_categories, "r")
        contents = file.read()
        self.categories = ast.literal_eval(contents)

        file = open(var.path_index_categories, "r")
        contents = file.read()
        self.index_categories = ast.literal_eval(contents)

    def print_message(self, row):
        print("Category is not in the item processed\n")
        print("date       amount       place")
        print(row["date"], " ", row["amount"], " ", row["place"])
        print("Next values are the categories presented:\n")
        for key in self.index_categories:
            print(key, ":", self.index_categories.get(key))

    def ask_category(self, row):
        Categories.print_message(self, row)
        value = input("Please enter a integer corresponding to the category:\n"
                      "if not there introduce the new category\n")
        return value

    def write_dictionary(self, dictionary: dict, path: str):
        a_file = open(path, "w")
        json.dump(dictionary, a_file)
        a_file.close()

    def verify_item_in_category(self):
        for index, row in self.outcome.iterrows():
            flag = False
            for key in self.categories.keys():
                list_places = self.categories.get(key)
                if row["place"] in list_places:
                    self.outcome.at[index, "category"] = str(key)
                    flag = True
            if not flag:
                value = Categories.ask_category(self, row)
                if len(value) <= 2:
                    value = self.index_categories.get(value)
                    list_places = self.categories.get(value)
                    if row["place"] not in list_places:
                        list_places.append(row["place"])
                    self.categories[value] = list_places
                else:
                    self.categories[value] = [row["place"]]
                    list_keys = list(self.index_categories.keys())
                    list_keys = [int(i) for i in list_keys]
                    list_keys.sort()
                    self.index_categories[str(list_keys[-1] + 1)] = value
                self.outcome.at[index, "category"] = value

        Categories.write_dictionary(self, self.categories, var.path_categories)
        Categories.write_dictionary(self, self.index_categories, var.path_index_categories)
        self.outcome.to_csv(var.path_outcome, mode='a', header=False, index=False)
