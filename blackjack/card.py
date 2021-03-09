# Remember to use docstrings in your classes and functions!

import PIL
from PIL import ImageTk
from PIL import Image
class Card:

    '''
    Class that stores all Card-images in a dict, as a class variable
    instances of Card = a particular Card, with suit, value, face, image
    '''

    #utility variables
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"
    card_sequence = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    card_values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,\
         "J": 10, "Q": 10, "K": 10, "A": 11}
    
    #class dict to store images
    card_images = {}

    def __init__(self, suit, value, face):
        self.suit = suit
        self.suitabbre = Card.abbre(suit)
        self._value = value
        self.face = face        #need the face, to differentiate between 10s
        self._image = Card.card_images[self.suitabbre + str(face)]  #search dict for the appropriate image
    
    @classmethod
    def abbre(cls, suit):   
        '''
        utility function, to link between diff representations of suits
        '''

        dict1 = {"clubs": "C", 1: "C", "diamonds":"D", \
            2: "D",  "hearts":"H", 3: "H", "spades":"S", 4: "S"}
        return dict1[suit]
    
    @property
    def value(self):
        value = self._value
        return value
    
    @value.setter
    def value(self, value):
        self._value = value
    
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, image):
        self._image = image
    
    @classmethod
    def load_images(cls):

        sample_deck = []

        target = ["CLUBS", "DIAMONDS", "HEARTS", "SPADES"]

        for i in range(1, 5):   #go from 1-4, to get suits
            suit = cls.abbre(i)
            for each in Card.card_sequence:
                #creating utility strings
                target_card = str(suit) + str(each)
                target_string = "images/"+ str(each) + str(suit) + ".jpg"   #assumes run program in folder blackjack

                #opening each image
                image = Image.open(target_string)
                resized = image.resize((120, 200),Image.ANTIALIAS)
                image = ImageTk.PhotoImage(resized)

                #create dict entry of image object
                Card.card_images[target_card] = None
                Card.card_images[target_card] = image   #key: Suit in "C", value in "1"
                
                #instantiating card objects for all cards
                result = getattr(Card, target[i-1])     #get the attribute of "CLUBS" and such, what spec weirdly asked for
                new_card = Card(result, Card.card_values[each], each)   #create new card instance
                sample_deck.append(new_card)
    
        return sample_deck      #returns array, of Card objects



    
