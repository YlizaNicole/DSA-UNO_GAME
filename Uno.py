#modification I want to change:
#turning the src in a single code
#adding the special wild card since the SRC isn't 
#According  to the rule decreasing the number of +4 cards cause there are only 4 



import tkinter as tk
from tkinter import messagebox
import random
from enum import Enum

CARD_HEIGHT = 100
CARD_WIDTH = 75
CARD_SPACE = 10

CARD_OVAL_COLOUR = "#fceee3"
CARD_BACK_BACKGROUND = "black"
CARD_BACK_FOREGROUND = "red"
CARD_BACK_TEXT_COLOUR = "yellow"
CARD_BACK_TEXT = "UNO++"

AI_DELAY = 2000


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


class Player:
    def __init__(self, name):
        self._name = name
        self._deck = Deck()

    def get_name(self):
        return self._name
    
    def get_deck(self):
        return self._deck

    def is_playable(self):
        raise NotImplementedError("is_playable to be implemented by subclasses")
    
    def has_won(self):
        if self._deck.get_amount() == 0:
            return True
        else:
            return False

    def pick_card(self, putdown_pile):
        raise NotImplementedError("pick_card to be implemented by subclasses")


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self._deck = Deck()

    def is_playable(self):
        return True

    def pick_card(self, putdown_pile):
        return None

class ComputerPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self._deck = Deck()

    def is_playable(self):
        return False

    def pick_card(self, putdown_pile): #BUG, Computer player can't activate Pick4Card effect
        for i in self._deck.get_cards():
            if i.matches(putdown_pile.top()):
                picked_card = i
                self._deck.get_cards().remove(i)
                return picked_card
        return None


class TurnManager:
    """
    A class to manage the order of turns amongst game players.
    """
    def __init__(self, players):
        """
        Construct a new turn manager to based on game players.

        Parameters:
             players (list<T>): An ordered list of players to store.
        """
        self._players = players
        # start in correct direction
        self._direction = True
        self._location = 0
        self._max = len(players)

    def current(self):
        """
        (T) Returns the player whose turn it is.
        """
        return self._players[self._location]

    def next(self):
        """
        (T) Moves onto the next players turn and return that player.
        """
        return self.skip(count=0)

    def peak(self, count=1):
        """
        Look forward or backwards in the current ordering of turns.

        Parameters:
            count (int): The amount of turns to look forward,
                         if negative, looks backwards.

        Returns:
            (T): The player we are peaking at.
        """
        location = self._location
        location += count if self._direction else -count
        location %= self._max
        return self._players[location]

    def reverse(self):
        """
        Reverse the order of turns.
        """
        self._direction = not self._direction

    def skip(self, count=0):
        """
        (T): Moves onto the next player, skipping 'count' amount players.
        """
        count += 1
        self._location += count if self._direction else -count
        self._location %= self._max
        return self._players[self._location]


class UnoGame:
    """
    A game of Uno++.
    """
    def __init__(self, deck, players):
        """
        Construct a game of uno from a pickup pile and list of players.

        Parameters:
            deck (Deck): The pile of cards to pickup from.
            players (list<Player>): The players in this game of uno.
        """
        self.pickup_pile = deck
        self.players = players

        self._turns = TurnManager(players)

        self.putdown_pile = Deck(self.pickup_pile.pick())
        self.special_pile = Deck()

        self._is_over = False
        self.winner = None

    def next_player(self):
        """
        Changes to the next player in the game and returns an instance of them.

        Returns:
            (Player): The next player in the game.
        """
        return self._turns.next()

    def current_player(self):
        """
        (Player) Returns the player whose turn it is currently.
        """
        return self._turns.current()

    def skip(self):
        """Prevent the next player from taking their turn."""
        self._turns.skip()

    def reverse(self):
        """Transfer the turn back to the previous player and reverse the order."""
        self._turns.reverse()

    def get_turns(self):
        """(TurnManager) Returns the turn manager for this game."""
        return self._turns

    def is_over(self):
        """
        (bool): True iff the game has been won. Assigns the winner variable.
        """
        for player in self.players:
            if player.has_won():
                self.winner = player
                self._is_over = True

        return self._is_over

    def select_card(self, player, card):
        """Perform actions for a player selecting a card

        Parameters:
            player (Player): The selecting player.
            card (Card): The card to select.
        """
        card.play(player, self)
        if card.__class__ in SPECIAL_CARDS:
            self.special_pile.add_card(card)
        else:
            self.putdown_pile.add_card(card)

    def take_turn(self, player):
        """
        Takes the turn of the given player by having them select a card.

        Parameters:
            player (Player): The player whose turn it is.
        """
        card = player.pick_card(self.putdown_pile)

        if card is None:
            player.get_deck().add_cards(self.pickup_pile.pick())
            return

        if card.matches(self.putdown_pile.top()):
            self.select_card(player, card)

    def take_turns(self):
        """
        Plays an entire round by taking the turn for each player in the game.
        """
        for player in self.players:
            self.take_turn(player)

            if player.has_won():
                return


def build_deck(structure, range_cards=(Card, )):
    """
    Construct a deck from a simplified deck structure.

    Example structure:
    [ (Card(colour=CardColour.red), (0, 10)),
      (SkipCard(colour=CardColour.green), (3, 5)) ]

    Creates a deck with red cards numbered from 0 up to but not including 10 and
    skip cards with the numbers 3 and 4. Assuming both cards are in range_cards,
    otherwise creates the same amount of cards with -1 as their numbers.

    Parameters:
        structure (list<tuple>): The simplified deck structure.
        range_cards (tuple<Card>): Cards whose numbers should be updated from -1.
    """
    deck = []

    for (card, (start, end)) in structure:
        for number in range(start, end):
            new_card = card.__class__(-1, card.get_colour())
            if card.__class__ in range_cards:
                new_card.set_number(number)
            deck.append(new_card)

    return deck

def generate_name():
    """
    (str): Selects a random name from a list of player names.
    """
    with open("players.txt", "r") as file:
        names = file.readlines()
    return random.choice(names).strip()



#DSA List

FULL_DECK = [
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

class CardView:
    """
    A class to manage the drawing of a Uno card on a canvas.
    """

    def __init__(self, canvas, left_side, oval_colour=CARD_OVAL_COLOUR,
                 background_colour=CARD_BACK_BACKGROUND,
                 foreground_colour=CARD_BACK_FOREGROUND,
                 text_colour=CARD_BACK_TEXT_COLOUR, text=CARD_BACK_TEXT):
        """
        Construct a new card to be drawn on the given canvas at the left_position.

        Parameters:
            canvas (tk.Canvas): The canvas to draw the card onto.
            left_side (int): The amount of pixels in the canvas to draw the card.
            oval_colour (tk.Color): Colour of the oval for this card.
            background_colour (tk.Color): Backface card background colour.
            foreground_colour (tk.Color): Backface card foreground colour.
            text_colour (tk.Color): Backface card text colour.
            text (str): Backface card text to display.
        """
        self._canvas = canvas

        self.left_side = left_side
        self.right_side = left_side + CARD_WIDTH

        self._oval_colour = oval_colour
        self._background = background_colour
        self._foreground = foreground_colour
        self._text_colour = text_colour
        self._text = text
        self._image = None

        self.draw()

CARD_ICONS = { #DSA Dictionary
    SkipCard: "skip",
    ReverseCard: "reverse"
}

class IconCardView(CardView):
    """
    A card that has an image associated with it.
    """

    def draw(self):
        """Draw the backface of the card to the canvas."""
        super().draw()
        self._image_view = None

    def redraw(self, card):
        """Redraw the card view with an icon.

        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        super().redraw(card)

        if card is not None:
            # clear text on the card
            self._canvas.itemconfig(self._text_view, text="")

            if self._image_view is None:
                # draw an image based on the card's class
                image = CARD_ICONS.get(card.__class__, "skip")
                self._image_view = self.draw_image(f"images/{image}.png")
            else:
                # show the image
                self._canvas.itemconfig(self._image_view, state="normal")
        else:
            if self._image_view is not None:
                # hide the image
                self._canvas.itemconfig(self._image_view, state="hidden")

class PickupCardView(CardView):
    """
    A card that displays the amount of cards to pickup.
    """

    def redraw(self, card):
        """Redraw the card view with the properties of the given card.

        Parameters:
            card (Card): The card to draw to the canvas. If None, draw the
                         backface of the card.
        """
        super().redraw(card)

        if card is not None:
            self._canvas.itemconfig(self._text_view,
                                    text=f"+{card.get_pickup_amount()}")

        
CARD_VIEWS = {
    SkipCard: IconCardView,
    ReverseCard: IconCardView,
    Pickup2Card: PickupCardView,
    Pickup4Card: PickupCardView
} #adding dictionary

