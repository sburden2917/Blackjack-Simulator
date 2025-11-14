import random
from constants import DEFAULT_NUM_DECKS

class Deck:
    def __init__(self, num_decks=DEFAULT_NUM_DECKS):
        self.num_decks = num_decks
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = []
        suits = ['♠', '♥', '♦', '♣']
        ranks = {
            'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
            '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10
        }
        for _ in range(self.num_decks):
            for suit in suits:
                for rank, value in ranks.items():
                    self.cards.append((value, rank + suit))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if not self.cards:
            # Deck is empty, reshuffle
            self.reset()
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)