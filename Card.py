class Card:
    def __init__(self, suit, value):
        names = ["jack", "queen", "king", "ace"]
        self.value = value
        self.suit = suit
        self.name = "card"
        if int(self.value) > 10:
            self.name = names[int(self.value) - 11]
        if self.name != "card" and self.name != "ace":
            self.value = 10
        if self.name == "ace":
            self.value = 11

        

    def print(self):
        if int(self.value) <= 10:
            return  "{}_of_{}.png".format(self.value, self.suit)
        return "{}_of_{}.png".format(self.name, self.suit)

    
