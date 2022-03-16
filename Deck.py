from Card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
        self.assemble()
    
    def assemble(self):
        for suit in ["spades", "hearts", "clubs", "diamonds"]:
            for value in range(2, 15):
                self.cards.append(Card(suit, value))
    
    def print(self):
        for card in self.cards:
            card.print()

    def shuffle(self):
        random.shuffle(self.cards)
    
    def hit(self):
        return self.cards.pop(0)

    def deal(self):
        retcards = [self.cards.pop(0), self.cards.pop(-1)]
        return retcards
