# Remember to use docstrings in your classes and functions!

from card import Card
import random 

class Deck:

    '''
    This class represents the current deck in use.
    It has methods 
    1: deal(), which deals the next card
    2: shuffle(), adds shuffled dealt-cards, to the bottom
    3: shuffle_this, utility function to shuffle a deck
    4: fill_deck(), calls Cards, to return a new deck of Card Objects
    '''

    def __init__(self):
        self.current_deck = []
        self.fill_deck()            #call fill_deck
        self.dealt_deck = []
    
    def fill_deck(self):
        '''
        function called at initialize to populate the deck
        '''
        first_deck = Card.load_images()
        shuffled = self.shuffle_this(first_deck)
        self.current_deck = shuffled
        pass
    
    @property
    def size(self):
        return len(self.current_deck)
    
    def shuffle(self):
        dealt_ed = self.shuffle_this(self.dealt_deck.copy())

        current = self.current_deck.copy()

        self.current_deck = dealt_ed + current  #as we pop from the end, we add to the start
        pass

    def shuffle_this(self, deck):
        random.shuffle(deck)
        
        return deck
    
    def deal(self):
        dealt = self.current_deck.pop(-1)   #one card at a time, from the back
        self.dealt_deck.append(dealt)
        if self.size == 13:             #initiates shuffle(), when fall to 13 cards in deck
            self.shuffle()
        return dealt
            

    
