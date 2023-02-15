from enum import Enum
from a2 import Card, SkipCard, ReverseCard, Pickup2Card, Pickup4Card

class CardColour(Enum):
    blue = "#508ebf"
    red = "#a30e15"
    yellow = "#f9bf3b"
    green = "#5d8402"
    black = "#222"


DECK = [
    (Card(0, CardColour.red), (0, 10)),
    (Card(0, CardColour.yellow), (0, 10)),
    (Card(0, CardColour.green), (0, 10)),
    (Card(0, CardColour.blue), (0, 10)),
]

SPECIAL_CARDS = [Pickup4Card]

print(DECK)