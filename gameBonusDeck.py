import random
from gameBonus import gameBonus

X1 = gameBonus("Country Road", "X1",
               "Double the base\nvalue of the\ncenter card\non your grid")

X2 = gameBonus("Haunted House", "X2",
               "(2)\nFor every card on\nyour grid that's\nadjacent to another card\nof the same faction")

X3 = gameBonus("Armored Fortress", "X3",
               "(6)\nFor every symbol group\nwhere you have more\nsymbols than opponent\nHands Eyes Bags")

X4 = gameBonus("Ranch Home", "X4",
               "(2)\nFor every card on\nyour grid with a base\nvalue of (2) or less")

X5 = gameBonus("Obelisk", "X5",
               "(2)\nFor each Red\non your grid")

X6 = gameBonus("Floating Castle", "X6",
               "(3)\nFor every unique faction\nin play on your grid")

X7 = gameBonus("Soldier's Armory", "X7",
               "(1)\nFor every 2 Hands\nin play")

X8 = gameBonus("Grave Yard", "X8",
               "(2)\nFor each Green\non your grid")

X9 = gameBonus("Dark Guillotine", "X9",
               "Choose:\n(4) For every face down\ncard in play\n________________\nImmediately gain (6)")

X10 = gameBonus("Ring Portal", "X10",
                "(4)\nFor each Blue Yellow\npair on your grid")


class gameBonusDeck:
    def __init__(self):
        self.deck = [X1, X2, X3, X4, X5,
                     X6, X7, X8, X9, X10]

    def __str__(self):
        deckStr = ""
        for card in self.deck:
            deckStr += card.__str__() + '\n'
        return deckStr

    def shuffle(self):
        random.shuffle(self.deck, random.random)

    def deal(self,id=''):
        if id=='':
            return self.deck.pop(0)
        else:
            return self.deck.pop([card.card_id for card in self.deck].index(id))

    def sort(self):
        self.deck.sort()

    def size(self):
        return len(self.deck)

    def addCards(self, cards):
        self.deck += cards
