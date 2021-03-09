# Remember to use docstrings in your classes and functions!

import tkinter as tk
from abc import ABC, abstractmethod
from deck import Deck
from hand import Hand
import sys

class GameGUI(ABC):

    def __init__(self, window):
        self._window = window
        self._canvas_width = 1024
        self._canvas_height = 400
        self._canvas = tk.Canvas(window, width=self._canvas_width, height=self._canvas_height)
        self._canvas.pack()
        window.bind("<Key>", self._keyboard_event)

    def _keyboard_event(self, event):
        key = str(event.char)

        if key == 'h':
            self.player_hit()
        elif key == 's':
            self.player_stand()
        elif key == 'r':
            self.reset()

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def player_hit(self):
        pass

    @abstractmethod
    def player_stand(self):
        pass


class BlackJack(GameGUI):

    '''
    This class is the main driver of the BlackJack game
    It controls initializing the Deck, dealing hands, evaluating the result, allowing users to play again etc
    '''

    def __init__(self, window):
        super().__init__(window)
        self.player_wins = 0
        self.dealer_wins = 0
        self.game_status = None
        self.new_session()
    
    @property
    def canvas(self):
        return self._canvas
    
    @canvas.setter
    def value(self, canvas):
        self._canvas = canvas
    
    @property
    def window(self):
        return self._window


    def new_session(self):
        '''
        called when start/restarting
        initializes deck
        creates hands, deals hands
        finishes by calling draw_it(), which GUI represents current game state
        '''
        self.canvas.delete("all")
        self.game_status = "In Progress . . ."
        self.game_status_color = "green"

        #initialize Deck
        new_deck = Deck()
        self.deck = new_deck

        #initialize Hands
        player_hand = Hand()
        self.player_hand = player_hand
        dealer_hand = Hand()
        self.dealer_hand = dealer_hand


        self.deal_first(new_deck, player_hand, dealer_hand) #deal first
        self.draw_it()  #GUI


        pass

    def deal_first(self, new_deck, player_hand, dealer_hand):
        '''
        assuming only two players, deals two to each in turn
        adds to the Hand object for each
        '''

        dealt1 = new_deck.deal()
        player_hand.add(dealt1)
        dealt2 = new_deck.deal()
        dealer_hand.add(dealt2)
        dealt3 = new_deck.deal()
        player_hand.add(dealt3)
        dealt4 = new_deck.deal()
        dealer_hand.add(dealt4)
        pass


    def draw_it(self):

        self.canvas.delete('all')

        global label_array      #to keep track of widgets created, for easier clearing
        label_array = []
        

        #utility variables
        player_hand = self.player_hand
        dealer_hand = self.dealer_hand

        player_hand_len = len(self.player_hand.holding)

        player_hand_total = str(self.player_hand.total)

        dealer_hand_len = len(self.dealer_hand.holding)

        dealer_hand_total = str(self.dealer_hand.total)

        column_num = max(player_hand_len , dealer_hand_len)


        #drawing GUI
        root = self.window

        canvas = self.canvas

        canvas.grid(row=8, column= 12 , padx=10, pady=10)        #padded grid, with spaces
        
        label1 = tk.Label(canvas, text ="Player Hand Total: %s"%player_hand_total)
        label1.grid(row=0, column=0, sticky='W')

        #drawing the player's hand
        global label_array1
        label_array1 = player_hand.draw(canvas, self.canvas, 0, 1, 120, 300)

        label3 = tk.Label(canvas, text ="Dealer Hand Total: %s"%dealer_hand_total)
        label3.grid(row=2, column=0, sticky='W')

        #drawing the dealer's hand
        global label_array2
        label_array2 = dealer_hand.draw(canvas, self.canvas, 0, 3, 120, 300)

        global label5
        label5 = tk.Label(canvas, text ="Game Status: %s"%self.game_status, fg=self.game_status_color)
        label5.grid(row=5, column=12)
        # label5.place(relx= 0.75, rely = 0.9)

        label6 = tk.Label(canvas, text ="Player Wins: %s"%self.player_wins)
        label6.grid(row=6, column=0, sticky='W')

        label7 = tk.Label(canvas, text ="Dealer Wins: %s"%self.dealer_wins)
        label7.grid(row=7, column=0, sticky='W')
        
        #populating label array
        label_array = [label1, label3, label5, label6, label7]

        for each in label_array1:
            label_array.append(each)
        
        for each in label_array2:
            label_array.append(each)
        pass
    
    def redraw(self):

        '''
        utility function, that allow clearing all widgets and drawing GUI again within a session
        '''
        global label_array
        for each in label_array:
            each.grid_forget()
        
        self.draw_it()

        pass


    def reset(self):
        '''
        utility function, resets all hands, clears all widgets, starts new session
        '''
        global label_array
        for each in label_array:
            each.grid_forget()
        self.canvas.delete("all")

        self.player_hand.reset()
        self.dealer_hand.reset()

        self.new_session()
        pass
    

    def player_hit(self):

        '''
        called when player "hits"
        deals card
        determines next time depending on how new card affected the player_hand total
        '''

        global label5

        dealt = self.deck.deal()
        self.player_hand.add(dealt)

        if self.player_hand.total <= 21:
            self.redraw()
        elif self.player_hand.total >= 22:
            self.game_status = "Dealer WINS... Press 'r' to start a new game"
            self.game_status_color = "red"
            label5.grid_forget()
            self.dealer_wins += 1
            self.redraw()
        pass

    def player_stand(self):
        '''
        called when player "stands"
        calls function to deal for dealer, as now dealer's turn
        '''
        self.deal_for_dealer()
        pass

    def deal_for_dealer(self):
        '''
        utility function
        deals for dealer as long as dealer_hand total less than 17, and less than 21
        calls different cases depending on how new card affects total
        '''

        if self.dealer_hand.total > 17 or self.dealer_hand.total >=21:
            self.who_won()
        else:
            while self.dealer_hand.total < 17:
                if self.dealer_hand.total > 21:
                    self.who_won()
                else:
                    dealt = self.deck.deal()
                    self.dealer_hand.add(dealt)
                    self.redraw()
            self.who_won()
        pass

    def who_won(self):
        '''
        utility function
        determines more complicated cases to decide who won the game
        '''
        global label5
        if (self.player_hand.total == self.dealer_hand.total) and (self.player_hand.total <= 21) and (self.dealer_hand.total<=21):
            self.game_status = "TIE Game ... Press 'r' to start a new game"
            self.game_status_color = "red"
            self.redraw()
        elif (self.player_hand.total == self.dealer_hand.total) and (self.player_hand.total > 21) and (self.dealer_hand.total<21):
            self.game_status = "TIE Game ... Press 'r' to start a new game"
            self.game_status_color = "red"
            self.redraw()
        elif self.dealer_hand.total > 21:
            self.game_status = "Player WINS... Press 'r' to start a new game"
            self.game_status_color = "red"
            self.player_wins += 1
            self.redraw()
        elif self.player_hand.total > self.dealer_hand.total:
            self.game_status = "Player WINS... Press 'r' to start a new game"
            self.game_status_color = "red"
            self.player_wins += 1
            self.redraw()
        elif self.player_hand.total < self.dealer_hand.total:
            self.game_status = "Dealer WINS... Press 'r' to start a new game"
            self.dealer_wins += 1
            self.game_status_color = "red"
            self.redraw()
        pass




def main():
    window = tk.Tk()
    window.title("Blackjack")
    # Uncomment this out when you are ready to implement BlackJack
    game = BlackJack(window)
    window.mainloop()


if __name__ == "__main__":
    main()
