import random
from gameCard import gameCard

R1 = gameCard("Plague Doctor", "R1", 1, "R", 1, 1, 1,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 1 for\neach Green in play")

R2 = gameCard("Tentacle Hentai", "R2", 2, "R", 0, 2, 0,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], True, "(Instant)\nBoth players discard a card\nfrom their grid and replace\nit with a random card from\nthe deck")

R3 = gameCard("Hooded Floater", "R3", 1, "R", 1, 1, 0,
              [[0, 1, 1],
               [0, 0, 1],
               [0, 1, 1]], False, "Double the base\nvalue of the\ncard to the left")

R4 = gameCard("The Usurper", "R4", 5, "R", 0, 2, 0,
              [[0, 2, 0],
               [1, 1, 1],
               [0, 2, 0]], True, "(Instant)\nYou may flip\nany card\non your grid")

R5 = gameCard("Bloody Mohawk", "R5", -4, "R", 3, 0, 0,
              [[0, 0, 0],
               [1, 0, 1],
               [1, 1, 1]], False, "Gain 1 for\neach Eye in play")

R6 = gameCard("Hand of God", "R6", 0, "R", 0, 1, 1,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 3 for each\nadjacent Red")

R7 = gameCard("Vape Lord", "R7", 3, "R", 1, 1, 1,
              [[0, 0, 0],
               [0, 2, 1],
               [0, 1, 1]], True, "(Instant)\nYou may discard a card\nfrom your grid and replace\nit with a random card\nfrom the deck")

R8 = gameCard("Loop Knight", "R8", -4, "R", 1, 1, 0,
              [[0, 1, 0],
               [2, 0, 2],
               [0, 1, 0]], True, "(Instant)\nFlip any card\non your\nopponent's grid")

R9 = gameCard("Tentacle Bomber", "R9", 4, "R", 1, 1, 0,
              [[0, 0, 1],
               [1, 1, 1],
               [1, 0, 0]], True, "(Instant)\nYou and your opponent\nboth draw a card")

R10 = gameCard("Orbsman", "R10", 0, "R", 0, 1, 1,
               [[1, 1, 1],
                [0, 0, 0],
                [0, 1, 0]], True, "(Instant)\nDraw 4 cards, then\nchoose one to add\nto your hand and\ndiscard the rest")

R11 = gameCard("Perfect Balance", "R11", 0, "R", 1, 1, 0,
               [[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]], False, "Gain 6 for each\nface down\ncard in play")

Y1 = gameCard("Cat Hostess", "Y1", 3, "Y", 0, 1, 1,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], True, "(Instant)\nFlip all face up cards\nin play with a value of\n(4) or higher")

Y2 = gameCard("Lock Picker", "Y2", 0, "Y", 0, 0, 3,
              [[1, 1, 0],
               [1, 1, 0],
               [0, 0, 0]], False, "Gain 3\nfor each (1)\nin play")

Y3 = gameCard("Scholar Bishop", "Y3", 1, "Y", 0, 1, 1,
              [[2, 1, 0],
               [1, 0, 1],
               [0, 1, 2]], False, "Gain 1 for each Bag\non your grid")

Y4 = gameCard("Bejeweled One", "Y4", 6, "Y", 0, 1, 0,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Lose 1 for each\nRed in the\nsame column")

Y5 = gameCard("Drunk Jester", "Y5", 0, "Y", 1, 0, 1,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], True, "(Instant)\nImmediately draw\n2 extra cards\nfrom the deck")

Y6 = gameCard("Three Chains", "Y6", 1, "Y", 0, 0, 3,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 2 for\nevery adjacent\nBlue or Yellow")

Y7 = gameCard("Crowned Hangman", "Y7", 0, "Y", 1, 0, 1,
              [[1, 0, 1],
               [0, 1, 0],
               [0, 0, 0]], False, "Gain 2 for each\nYellow in this row")

Y8 = gameCard("Masked King", "Y8", 5, "Y", 0, 0, 2,
              [[0, 0, 0],
               [0, 0, 0],
               [1, 2, 1]], True, "(Instant)\nYou may flip any\nface down cards\non your grid")

Y9 = gameCard("Hammer Junior", "Y9", 3, "Y", 2, 0, 1,
              [[0, 0, 1],
               [0, 1, 0],
               [1, 0, 0]], False, "Gain 1\nfor each Blue\nin play")

Y10 = gameCard("Village Mob", "Y10", 1, "Y", 0, 0, 3,
               [[0, 0, 0],
                [0, 1, 1],
                [0, 1, 1]], False, "Gain 2\nfor each (0)\nin play")

Y11 = gameCard("Hammer Senior", "Y11", 10, "Y", 1, 0, 1,
               [[1, 0, 0],
                [0, 0, 0],
                [0, 0, 1]], False, "Lose 1 for each\nRed in play")

G1 = gameCard("Rock Sitter", "G1", 4, "G", 0, 2, 0,
              [[1, 0, 0],
               [0, 0, 0],
               [0, 0, 1]], False, "Gain 1 for each\nGreen in play")

G2 = gameCard("Neck Slicer", "G2", 1, "G", 2, 1, 0,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 3\nfor every adjacent\nRed or Green")

G3 = gameCard("Bear Bear", "G3", 3, "G", 0, 1, 1,
              [[1, 0, 0],
               [1, 0, 0],
               [1, 0, 0]], False, "If you have 3 Green on your grid:\nYou may rotate this card\n180 degrees: It's now a copy\nof the card to its\nimmediate right")

G4 = gameCard("Crowned Archer", "G4", 4, "G", 0, 0, 1,
              [[1, 1, 2],
               [0, 0, 0],
               [2, 1, 1]], True, "(Instant)\nDiscard a card from your\nhand, draw the top 3 cards\nfrom the deck, then\npick one to replace it")

G5 = gameCard("Were Wolf", "G5", 2, "G", 0, 3, 0,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "During scoring phase:\nyou may flip this card\nif you choose")

G6 = gameCard("Horned Shaman", "G6", 1, "G", 0, 1, 1,
              [[0, 0, 0],
               [1, 1, 1],
               [0, 0, 0]], False, "Double the base value\nof the card above this one\nduring scoring\nphase. You may flip the\ncard below it")

G7 = gameCard("Horn Blower", "G7", 5, "G", 2, 1, 0,
              [[1, 0, 0],
               [0, 1, 2],
               [2, 0, 0]], True, "(Instant)\nYou may move a card\non your grid to another\nopen position")

G8 = gameCard("Bird Master", "G8", 0, "G", 1, 1, 1,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 2 for each\nEye in this column")

G9 = gameCard("Boy Knight", "G9", 1, "G", 0, 0, 2,
              [[0, 0, 1],
               [0, 1, 0],
               [0, 0, 1]], False, "Gain 1 for\nevery Hand\non your grid")

G10 = gameCard("Bald Necromancer", "G10", 3, "G", 0, 1, 1,
               [[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]], False, "Gain 3 for each\nGreen Red pair on\nyour grid")

G11 = gameCard("Groot", "G11", 9, "G", 0, 3, 0,
               [[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]], False, "Flip any adjacent\nBlue or Yellow")

B1 = gameCard("Potion Seller", "B1", -3, "B", 0, 2, 0,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 1 for each\nBag on your grid")

B2 = gameCard("Dark Horseman", "B2", 6, "B", 1, 0, 0,
              [[1, 1, 1],
               [1, 0, 1],
               [1, 1, 1]], False, "")

B3 = gameCard("Princess Spear", "B3", 2, "B", 1, 1, 0,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 1 for each\nAdjacent Blue")

B4 = gameCard("Traveling Librarian", "B4", 3, "B", 1, 1, 0,
              [[2, 1, 2],
               [1, 1, 1],
               [2, 1, 2]], False, "This card gains\n3 Eyes")

B5 = gameCard("Armored Bride", "B5", 1, "B", 0, 1, 1,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 1 for every 2 Hands\nin play")

B6 = gameCard("Lamp Lighter", "B6", 4, "B", 1, 0, 1,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Lose 1 for each\nadjacent Red")

B7 = gameCard("Scythe Slasher", "B7", 1, "B", 1, 2, 0,
              [[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1]], False, "In play:\n<8 Hands X=(1)\n8+ Hands X=(5)\n12+ Hands X=(8)")

B8 = gameCard("Kneeling Warrior", "B8", 3, "B", 1, 0, 1,
              [[1, 0, 0],
               [2, 0, 0],
               [1, 1, 2]], False, "Gain 1 for each\n(1) on your grid")

B9 = gameCard("Shielded Flailer", "B9", 0, "B", 1, 0, 1,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, "Gain 2 for each\nBlue on your grid")

B10 = gameCard("Big Sword", "B10", 4, "B", 3, 0, 0,
               [[1, 1, 1],
                [0, 0, 0],
                [0, 0, 0]], False, "")

B11 = gameCard("Ponytail Blacksmith", "B11", 2, "B", 1, 0, 1,
               [[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]], False, "Gain 1 for each\nHand in this row")


class gameDeck:
    def __init__(self):
        
        all_cards = [R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11,
                     Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8, Y9, Y10, Y11,
                     G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11,
                     B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11]
        self.deck = [card.__copy__() for card in all_cards]

    def __str__(self):
        deckStr = ""
        for card in self.deck:
            deckStr += card.__str__() + '\n'
        return deckStr

    def shuffle(self):
        random.shuffle(self.deck, random.random)

    def deal(self):
        return self.deck.pop(0)

    def sort(self):
        self.deck.sort()

    def size(self):
        return len(self.deck)

    def addCards(self, cards):
        self.deck += cards
