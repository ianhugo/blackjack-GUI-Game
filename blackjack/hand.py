# Remember to use docstrings in your classes and functions!
import tkinter as tk

class Hand:
    '''
    This class represents the hand of a particular player/dealer
    It holds the Card objects that are in said hand
    supports adding add(), reseting  reset() the hand
    supports draw(), which output a tkinter GUI representation of the current Hand
    '''

    def __init__(self):
        self.holding = []
    

    def reset(self):
        self.holding = []
        pass

    def add(self, card):
        self.holding.append(card)
        pass

    @property
    def total(self):
        total = 0

        for each_card in self.holding:
            new_value = each_card.value
            total = total + new_value

        return total

    def draw(self, root, canvas, start_x, start_y, canvas_width, canvas_height):
        label_array = []
        print(self.holding)
        for i in range(len(self.holding)):
            label = tk.Label(root, image= self.holding[i].image)
            label.image = self.holding[i]
            label.grid(row=start_y, column=i)
            label_array.append(label)

        return label_array
        

