import random

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        # A standard deck has 52 cards: 4 suits of 13 ranks
        # For Blackjack, suit doesn't matter, only rank value
        # Ranks: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
        # Values: A=1/11, 2-9=face value, 10/J/Q/K=10
        ranks = [(i, str(i)) for i in range(2, 11)] + \
                [(10, 'J'), (10, 'Q'), (10, 'K')] + \
                [(1, 'A')] # Ace value is 1 initially, can be 11

        # Create 4 copies of each rank for a single deck
        self.cards = ranks * 4
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if not self.cards:
            print("Reshuffling deck...")
            self.reset() # Reshuffle if deck runs out
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)