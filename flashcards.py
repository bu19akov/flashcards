from random import choice
from io import StringIO
import argparse


class FlashCard:

    def __init__(self):
        self.flashcards = dict()
        self.logs = StringIO()

    def add_card(self):
        term = self.input_("The card:\n")
        while term in self.flashcards.keys():
            term = self.input_(f'The term "{term}" already exists. Try again:\n')
        definition = self.input_("The definition of the card:\n")
        definitions = [i[0] for i in self.flashcards.values()]
        while definition in definitions:
            definition = self.input_(f'The definition "{definition}" already exists. Try again:\n')
        self.flashcards[term] = [definition, 0]
        self.print_(f'The pair ("{term}":"{definition}") has been added')

    def remove_card(self):
        card = self.input_("Which card?\n")
        if card in self.flashcards.keys():
            del self.flashcards[card]
            self.print_("The card has been removed.")
        else:
            self.print_(f'Can\'t remove "{card}": there is no such card.')

    def import_cards(self, import_file=""):
        file_name = self.input_("File name:") if import_file == "" else import_file
        try:
            with open(file_name, "r") as file:
                counter = 0
                for line in file:
                    pair = line.split()
                    if pair[0] in self.flashcards.keys():
                        del self.flashcards[pair[0]]
                    self.flashcards[pair[0]] = [pair[1], int(pair[2])]
                    counter += 1
                self.print_(f"{counter} cards have been loaded.")
        except FileNotFoundError:
            self.print_("File not found.")

    def export_cards(self, export_file=""):
        file_name = self.input_("File name:") if export_file == "" else export_file
        with open(file_name, "w") as file:
            for term, definition in self.flashcards.items():
                file.write(term + " " + definition[0] + " " + str(definition[1]) + "\n")
            self.print_(f"{len(self.flashcards)} cards have been saved.")

    def user_ask(self):
        number = int(self.input_("How many times to ask?\n"))
        for i in range(number):
            term = choice(list(self.flashcards.keys()))
            values = [i[0] for i in self.flashcards.values()]
            self.print_(f'Print the definition of "{term}":')
            user_definition = self.input_()
            if user_definition == self.flashcards[term][0]:
                self.print_("Correct!")
            elif user_definition != self.flashcards[term][0] and user_definition in values:
                right_term = list(self.flashcards.keys())[values.index(user_definition)]
                self.print_(f'Wrong. The right answer is "{self.flashcards[term][0]}", but your definition is correct for "{right_term}".')
                self.flashcards[term][1] += 1
            else:
                self.print_(f'Wrong. The right answer is "{self.flashcards[term][0]}".')
                self.flashcards[term][1] += 1

    def save_log(self):
        file_name = self.input_("File name:\n")
        with open(file_name, "w") as log:
            for line in self.logs.getvalue():
                log.write(line)
        self.print_("The log has been saved.")

    def hardest_card(self):
        maximum = 1
        hardest = list()
        for term, definition in self.flashcards.items():
            if definition[1] > maximum:
                maximum = definition[1]
                hardest.clear()
                hardest.append(term)
            elif definition[1] == maximum:
                hardest.append(term)
        if len(hardest) == 1:
            self.print_(f'The hardest card is "{hardest[0]}". You have {maximum} errors answering it.')
        elif len(hardest) > 1:
            cards = ", ".join([f'"{i}"' for i in hardest])
            self.print_(f'The hardest cards are {cards}. You have {maximum} errors answering them.')
        else:
            self.print_("There are no cards with errors.")

    def reset_stats(self):
        for term, definition in self.flashcards.items():
            definition[1] = 0
        self.print_("Card statistics have been reset.")

    def print_(self, line):
        print(line)
        self.logs.write(line + "\n")

    def input_(self, line=""):
        s = input(line)
        self.logs.write(line)
        self.logs.write(s + "\n")
        return s

    def check_action(self):
        while True:
            action = self.input_("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
            if action == "exit":
                print("Bye bye!")
                break
            elif action == "add":
                self.add_card()
            elif action == "remove":
                self.remove_card()
            elif action == "import":
                self.import_cards()
            elif action == "export":
                self.export_cards()
            elif action == "ask":
                self.user_ask()
            elif action == "log":
                self.save_log()
            elif action == "hardest card":
                self.hardest_card()
            elif action == "reset stats":
                self.reset_stats()


parser = argparse.ArgumentParser(description="This program creates flashcards to improve your learning process")
parser.add_argument("-i", "--import_from", help="Specify the file from which you want to import flashcards")
parser.add_argument("-e", "--export_to", help="Specify the file to which you want to export flashcards")
args = parser.parse_args()
f = FlashCard()
if args.import_from:
    f.import_cards(args.import_from)
f.check_action()
if args.export_to:
    f.export_cards(args.export_to)
