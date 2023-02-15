#modification I want to change:
#turning the src in a single code
#adding the special wild card since the SRC isn't 




import random
from enum import Enum

#build a deck w colors
class CardColor(Enum):
    blue = "#0956BF"
    red = "#D72600"
    yellow = "#ECD407"
    green = "#379711"
    black = "#222"

class Card:
    def __init__(self, number, colour):
        self._number = number
        self._colour = colour
        self._amount = 0

    def get_number(self):
        return self._number

    def set_number(self, number):
        self._number = number

    def get_colour(self):
        return self._colour

    def set_colour(self, colour):
        self._colour = colour
    
    def get_pickup_amount(self):
        return self._amount

class SkipCard(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)
        
    def play(self, game):
        game.skip()

class ReverseCard(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)

    def play(self, game):
        game.reverse()


Deck = [
    Card(0, CardColor.red), (0, 10),
    Card(0, CardColor.yellow), (0, 10),
    Card(0, CardColor.green), (0, 10),
    Card(0, CardColor.blue), (0, 10),
    Card(0, CardColor.red), (1, 10),
    Card(0, CardColor.yellow), (1, 10),
    Card(0, CardColor.green), (1, 10),
    Card(0, CardColor.blue), (1, 10),

    SkipCard(0, CardColor.red), (0, 2),
    SkipCard(0, CardColor.yellow), (0, 2),
    SkipCard(0, CardColor.green), (0, 2),
    SkipCard(0, CardColor.blue), (0, 2),

    (ReverseCard(0, CardColor.red), (0, 2)),
    (ReverseCard(0, CardColor.yellow), (0, 2)),
    (ReverseCard(0, CardColor.green), (0, 2)),
    (ReverseCard(0, CardColor.blue), (0, 2)),

    
]

print(Deck)