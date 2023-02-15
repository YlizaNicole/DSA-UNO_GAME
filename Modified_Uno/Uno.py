#modification I want to change:
#turning the src in a single code
#adding the special wild card since the SRC isn't 
#According  to the rule decreasing the number of +4 cards cause there are only 4 




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

    def matches(self, card):
        if isinstance(card, Pickup4Card): #When starting game with special cards
            return True
        if self._colour == card.get_colour() or self._number == card.get_number():
            return True
        return False

    def play(self):
        return 0

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

class Pickup2Card(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)
        self._amount = 2
    
    def get_pickup_amount(self):
        return self._amount

    def play(self, game):
        cards = game.pickup_pile.pick(self._amount)
        game.next_player().get_deck().add_cards(cards)
        game._turns._location = game._turns._location-1


class Pickup4Card(Card):
    def __init__(self, number, colour):
        Card.__init__(self, number, colour)
        self._amount = 4
    
    def get_pickup_amount(self):
        return self._amount

    def matches(self, putdown_pile):
        return True

    def play(self, game):
        cards = game.pickup_pile.pick(self._amount)
        game.next_player().get_deck().add_cards(cards)
        game._turns._location = game._turns._location-1

class Deck:
    def __init__(self, starting_cards = None):
        if starting_cards == None:
            self._cards = [] #DSA empty list
        else:
            self._cards = [] # DSA empty list
            self._cards.extend(starting_cards) #DSA List Methods & Built-In FunctIons extend()
 
    def get_cards(self):
        return self._cards
    
    def get_amount(self):
        return len(self._cards) #DSA using List Methods & Built-In FunctIons len ()

    def shuffle(self):
        random.shuffle(self._cards)

    def pick(self, amount = 1):
        picked_cards = [] # DSA empty list
        for i in range(0, amount):
            picked_cards.append(self._cards[i]) #DSA List Methods & Built-In FunctIons append ()
        for i in range(0, amount):
            del self._cards[i]
        return picked_cards

    def add_card(self, card):
        self._cards.append(card) #DSA List Methods & Built-In FunctIons

    def add_cards(self, cards):
        self._cards.extend(cards) #DSA List Methods & Built-In FunctIons extend()

    def top(self):
        if len(self._cards) == 0: #DSA using List Methods & Built-In FunctIons len ()
            return None
        else:
            #DSA using List Methods & Built-In FunctIons len ()
            return self._cards[len(self._cards)-1]


#DSA List

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

    ReverseCard(0, CardColor.red), (0, 2),
    ReverseCard(0, CardColor.yellow), (0, 2),
    ReverseCard(0, CardColor.green), (0, 2),
    ReverseCard(0, CardColor.blue), (0, 2),

    Pickup2Card(0, CardColor.red), (0, 2),
    Pickup2Card(0, CardColor.yellow), (0, 2),


    Pickup4Card(0, CardColor.black), (0, 2),
    Pickup4Card(0, CardColor.black), (0, 2),

    #modifed to have the change color wild card

    ]

SPECIAL_CARDS = [Pickup4Card]

print(Deck)
print (SPECIAL_CARDS)